import pandas as pd
import numpy as np


def fill_missing_values(df, cols_to_fill):
    """
    Fill missing values in specified columns by grouping by 'Name' and using the first non-null value within each group.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame containing the data to be processed
    cols_to_fill : list
        List of column names where missing values should be filled
        
    Returns:
    --------
    pandas.DataFrame
        The DataFrame with missing values filled in the specified columns
        
    Raises:
    -------
    ValueError
        If 'Name' column is missing from the DataFrame
        If any column in cols_to_fill is missing from the DataFrame
    """

    # Input validation
    if 'Name' not in df.columns:
        raise ValueError("The DataFrame must contain a 'Name' column for grouping")
    
    missing_cols = [col for col in cols_to_fill if col not in df.columns]
    if missing_cols:
        raise ValueError(f"The following columns are missing from the DataFrame: {missing_cols}")
    
    print(f"Missing values before filling:\n{df[cols_to_fill].isna().sum()}")

    # Group by game name and fill missing values with the first non-null value in the group
    for col in cols_to_fill:
        df[col] = df.groupby('Name')[col].transform(
            lambda x: x.fillna(x.dropna().iloc[0]) if not x.dropna().empty else x
        )

    print(f"\nMissing values before filling:\n{df[cols_to_fill].isna().sum()}")
    
    return df