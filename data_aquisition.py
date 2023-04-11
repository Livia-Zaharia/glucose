import pandas as pd
from pathlib import Path


class GetData:

    def cvs_insert(self, file_name:str):
        """
        Function that inserts from the cvs , removes nulls and renames some column title.
        It needs the Pandas import to work and also the Path library.
        """

        p=Path.cwd()
        p=p/file_name

        df=pd.read_csv(p, index_col=0)

        glucose=df[['Timestamp (YYYY-MM-DDThh:mm:ss)','Glucose Value (mg/dL)']]

        glucose['Timestamp (YYYY-MM-DDThh:mm:ss)']=pd.to_datetime(glucose['Timestamp (YYYY-MM-DDThh:mm:ss)'])
    
        glucose['Glucose Value (mg/dL)']=pd.to_numeric(glucose['Glucose Value (mg/dL)'],errors='coerce')
    
        glucose.dropna(inplace=True)  

        glucose['Glucose Value (mg/dL)']=glucose['Glucose Value (mg/dL)'].astype(float)
        glucose= glucose.rename(columns={'Timestamp (YYYY-MM-DDThh:mm:ss)':'Timestamp'})

        return glucose
    