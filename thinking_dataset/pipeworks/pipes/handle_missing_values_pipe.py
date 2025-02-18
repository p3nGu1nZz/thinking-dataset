# @file project_root/thinking_dataset/pipes/handle_missing_values_pipe.py
# @description Defines HandleMissingValuesPipe for handling missing values.
# @version 1.0.0
# @license MIT

import pandas as pd
from .pipe import Pipe
from thinking_dataset.utils.log import Log


class HandleMissingValuesPipe(Pipe):
    """
    Pipe to handle missing values in the DataFrame.
    """

    def flow(self, df: pd.DataFrame, **args) -> pd.DataFrame:
        columns = self.config.get("columns")
        remove_partials = self.config.get("remove_partials", True)
        allow_empty = self.config.get("allow_empty", False)
        initial_length = len(df)

        if "auto" in columns:
            Log.info("Auto-detecting columns for missing values check")
            columns = df.columns.tolist()

        Log.info("Starting HandleMissingValuesPipe")
        Log.info(f"Initial number of rows: {initial_length}")
        Log.info(f"Columns to check for missing values: {columns}")
        Log.info(f"Remove partials: {remove_partials}")
        Log.info(f"Allow empty: {allow_empty}")

        if "auto" not in columns:
            missing_columns = [col for col in columns if col not in df.columns]
            if missing_columns:
                raise KeyError("Missing columns for missing "
                               f"values check: {missing_columns}")

        if remove_partials:
            if not allow_empty:
                for col in columns:
                    Log.info(f"Processing column: {col}")
                    df[col] = df[col].replace(r'^\s*$', pd.NA, regex=True)
            df = df.dropna(subset=columns)

        final_length = len(df)
        removed_count = initial_length - final_length

        Log.info(f"Removed {removed_count} rows with missing values")
        Log.info(f"Final number of rows: {final_length}")
        Log.info("Finished HandleMissingValuesPipe")

        return df
