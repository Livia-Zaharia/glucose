from pathlib import Path
from ripple import Ripple
import pandas as pd
import typing as t

from constants import ANALYSIS_XLSX_FILE_NAME
from data_division import Divide

CURRENT_PATH_CWD = Path.cwd()


class Display:

    def write_analysis_to_xls_file(self, summary_list, sheet_name):
        with pd.ExcelWriter(CURRENT_PATH_CWD / ANALYSIS_XLSX_FILE_NAME, engine="xlsxwriter") as writer:

            df = pd.DataFrame(summary_list)
            df.to_excel(writer, sheet_name=sheet_name, index=False, header=True, engine="xlsxwriter")


    def batch_write_images_to_disk(self, ripple_list:t.List[Ripple]):
        for x in range(len(ripple_list)):
            ripple_list[x].create_graphic(x,False)



