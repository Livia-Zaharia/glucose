"""
Data acquisition module that imports the data from the csv

"""
from pathlib import Path

import pandas as pd

CURRENT_PATH_CWD = Path.cwd()


class GetData:
    """
    Class of method(s) for getting data
    """

    def get_data(self, file_name: str) -> pd.DataFrame:
        """
        Method that creates a dataframe from the cvs, further processes by removing nulls and renames column titles.
        Assumes the file name is at the same path as this file.
        It needs the Pandas import to work and also the Path library.
        Raises: if the input csv file is missing or corrupted
        """
        file_path = CURRENT_PATH_CWD / file_name

        if not file_path.exists():
            raise Exception(f'The expected input file name does not exist at path: {file_path}')

        df = pd.read_csv(filepath_or_buffer=file_path, index_col=0)

        glucose = df[['Timestamp (YYYY-MM-DDThh:mm:ss)', 'Glucose Value (mg/dL)']]

        glucose['Timestamp (YYYY-MM-DDThh:mm:ss)'] = pd.to_datetime(glucose['Timestamp (YYYY-MM-DDThh:mm:ss)'])

        glucose['Glucose Value (mg/dL)'] = pd.to_numeric(glucose['Glucose Value (mg/dL)'], errors='coerce')

        glucose.dropna(inplace=True)

        glucose['Glucose Value (mg/dL)'] = glucose['Glucose Value (mg/dL)'].astype(float)
        glucose = glucose.rename(columns={'Timestamp (YYYY-MM-DDThh:mm:ss)': 'Timestamp'})

        return glucose
