import numpy as np
import pandas as pd
from otlang.sdk.syntax import Keyword, Positional, OTLType
from pp_exec_env.base_command import BaseCommand, Syntax


class DivideCommand(BaseCommand):
    """
    Makes division of two columns of dataframe
    a, b - columns must be divided
    | divide a b - creates a new df

    | divide a b as c - creates new column "c" in the old df
    """

    syntax = Syntax(
        [
            Positional("dividend", required=True, otl_type=OTLType.ALL),
            Positional("divisor", required=True, otl_type=OTLType.ALL),
        ],
    )
    use_timewindow = False  # Does not require time window arguments
    idempotent = True  # Does not invalidate cache

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.log_progress("Start divide command")
        # that is how you get arguments
        dividend_argument = self.get_arg("dividend")
        if isinstance(dividend_argument.value, str):
            dividend = df[dividend_argument.value]
        else:
            dividend = dividend_argument.value

        divisor_argument = self.get_arg("divisor")
        if isinstance(divisor_argument.value, str):
            divisor = df[divisor_argument.value]
        else:
            divisor = divisor_argument.value
        result_column_name = divisor_argument.named_as

        if isinstance(dividend, (int, float)) and isinstance(divisor, (int, float)):
            if result_column_name != "" and not df.empty:
                dividend = np.array([dividend] * df.shape[0])
                divisor = np.array([divisor] * df.shape[0])
            else:
                dividend = np.array([dividend])
                divisor = np.array([divisor])

        self.logger.debug(f"Command add get dividend = {dividend}")
        self.logger.debug(
            f"Command add get divisor = {divisor}"
        )

        if result_column_name != "":
            df[result_column_name] = dividend / divisor
            self.logger.debug(f"New column name: {result_column_name}")

        else:
            df = pd.DataFrame(
                {
                    f"divide_{divisor_argument.value}_{dividend_argument.value}": dividend / divisor
                }
            )
        self.log_progress("Division is completed.", stage=1, total_stages=1)
        return df
