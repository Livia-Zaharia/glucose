"""
Module for exporting and displaying data. It works on the display functions which are not covered 
by the Database Manager or used in conjencture with the methods of class Ripple.
It can be used as standalone provided the values asked
"""

from pathlib import Path
from ripple import Ripple
import pandas as pd
import typing as t

from constants import ANALYSIS_XLSX_FILE_NAME
from data_division import Divide

CURRENT_PATH_CWD = Path.cwd()
IMAGES_PATH = CURRENT_PATH_CWD / "images_and_graphs"


class Display:
    """
    Class of methods to arrange the data into user friendly formats
    """

    def write_analysis_to_xls_file(self, summary_list:t.List, sheet_name:str) -> None:
        """
        Method of writting a simple list to an xlsx file
        """
        with pd.ExcelWriter(CURRENT_PATH_CWD / ANALYSIS_XLSX_FILE_NAME, engine="xlsxwriter") as writer:

            df = pd.DataFrame(summary_list)
            df.to_excel(writer, sheet_name=sheet_name, index=False, header=True, engine="xlsxwriter")


    def batch_write_graphs_to_disk(self, ripple_list:t.List[Ripple], flag:bool):
        """
        Method of batch writing files in png or html format flag= True writes html else writes png
        """
 
        for x in range(len(ripple_list)):

            DATA_PATH=IMAGES_PATH/f"Ripple_no{x}"
            DATA_PATH.mkdir(parents=True,exist_ok=True)

            ripple_list[x].create_graphic(x,flag)



