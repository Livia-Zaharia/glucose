"""
Data acquisition module that imports the data from the csv
"""

from pathlib import Path

import pandas as pd

CURRENT_PATH_CWD = Path.cwd()


def read_csv_file(file_name: str) -> pd.DataFrame:
    """
    Read the input CSV file and return the DataFrame.

    Args:
        file_name: The name of the input CSV file.

    Returns:
        A Pandas DataFrame containing the CSV data.

    Raises:
        Exception: If the input CSV file is missing or corrupted.
    """
    # Combine the current working directory path with the file name
    file_path = CURRENT_PATH_CWD / file_name

    # Check if the file exists
    if not file_path.exists():
        # Raise an exception if the file is missing
        raise Exception(f'The expected input file name does not exist at path: {file_path}')

    # Read the CSV file and return the DataFrame
    df = pd.read_csv(filepath_or_buffer=file_path, index_col=0)

    return df


def get_insulin_data(file_name: str) -> pd.DataFrame:
    """
    Create a dataframe containing insulin data from a given CSV file, preprocess it by removing nulls and renaming columns.

    Args:
        file_name: The name of the input CSV file.

    Returns:
        A preprocessed Pandas DataFrame containing insulin data.

    Raises:
        Exception: If the input CSV file is missing or corrupted.
    """
    # Read the CSV file and store it in a DataFrame
    df = read_csv_file(file_name=file_name)
    # Preprocess the insulin data and return the resulting DataFrame
    insulin = _preprocess_insulin_data(df=df)

    return insulin


def get_glucose_data(file_name: str) -> pd.DataFrame:
    """
    Create a dataframe containing glucose data from a given CSV file, preprocess it by removing nulls and renaming columns.

    Args:
        file_name: The name of the input CSV file.

    Returns:
        A preprocessed Pandas DataFrame containing glucose data.

    Raises:
        Exception: If the input CSV file is missing or corrupted.
    """
    # Read the CSV file and store it in a DataFrame
    df = read_csv_file(file_name=file_name)
    # Preprocess the glucose data and return the resulting DataFrame
    glucose = _preprocess_glucose_data(df=df)

    return glucose


def _preprocess_glucose_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the DataFrame containing glucose data by removing nulls and renaming columns.

    Args:
        df: A Pandas DataFrame containing the glucose data.

    Returns:
        A preprocessed Pandas DataFrame containing glucose data.
    """
    # Select the relevant columns from the input DataFrame
    glucose = df[['Timestamp (YYYY-MM-DDThh:mm:ss)', 'Glucose Value (mg/dL)']]

    # Convert the timestamp column to datetime format
    glucose['Timestamp (YYYY-MM-DDThh:mm:ss)'] = pd.to_datetime(glucose['Timestamp (YYYY-MM-DDThh:mm:ss)'])

    # Convert the glucose value column to numeric, setting any errors to NaN
    glucose['Glucose Value (mg/dL)'] = pd.to_numeric(glucose['Glucose Value (mg/dL)'], errors='coerce')

    # Remove rows with missing values
    glucose.dropna(inplace=True)

    # Convert the glucose value column to float data type
    glucose['Glucose Value (mg/dL)'] = glucose['Glucose Value (mg/dL)'].astype(float)

    # Rename the timestamp column for better readability
    glucose.rename(columns={'Timestamp (YYYY-MM-DDThh:mm:ss)': 'Timestamp'}, inplace=True)

    return glucose


def _preprocess_insulin_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the DataFrame containing insulin data by removing nulls and renaming columns.

    Args:
        df: A Pandas DataFrame containing the insulin data.

    Returns:
        A preprocessed Pandas DataFrame containing insulin data.
    """
    # Select the relevant columns from the input DataFrame
    insulin = df[['Timestamp (YYYY-MM-DDThh:mm:ss)', 'Event Subtype', 'Insulin Value (u)']]

    # Convert the timestamp column to datetime format
    insulin['Timestamp (YYYY-MM-DDThh:mm:ss)'] = pd.to_datetime(insulin['Timestamp (YYYY-MM-DDThh:mm:ss)'])

    # Convert the insulin value column to numeric, setting any errors to NaN
    insulin['Insulin Value (u)'] = pd.to_numeric(insulin['Insulin Value (u)'], errors='coerce')

    # Remove rows with missing values
    insulin.dropna(inplace=True)

    # Convert the insulin value column to float data type
    insulin['Insulin Value (u)'] = insulin['Insulin Value (u)'].astype(float)

    # Rename the columns for better readability
    insulin.rename(
        columns={'Timestamp (YYYY-MM-DDThh:mm:ss)': 'Timestamp', 'Event Subtype': 'Type', 'Insulin Value (u)': 'Value'},
        inplace=True)

    return insulin
