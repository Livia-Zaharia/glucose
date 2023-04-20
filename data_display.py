from pathlib import Path

import pandas as pd

from constants import ANALYSIS_XLSX_FILE_NAME
from data_division import Divide

CURRENT_PATH_CWD = Path.cwd()


class Display:
    def __init__(self, r_list, ripple_connections):
        self.ripple_list = r_list
        self.ripple_connections = ripple_connections

    def write_analysis_to_xls_file(self):
        with pd.ExcelWriter(CURRENT_PATH_CWD / ANALYSIS_XLSX_FILE_NAME, engine="xlsxwriter") as writer:
            summary_list = []

            for item in self.ripple_connections:
                percent, position_from, position_to = item[-1]
                summary_list.append(f"from {position_from} to {position_to} there is a {round((percent) * 100)}% match")

            df = pd.DataFrame(summary_list)
            df.to_excel(writer, sheet_name="pattern comparison summary", index=False, header=True, engine="xlsxwriter")

            for x, item in enumerate(self.ripple_connections):
                sheet_name = f"{x} matching"
                data = item
                df2 = pd.DataFrame(data, columns=["percentage match", "starting from", "compared with"])
                df2.to_excel(writer, sheet_name=sheet_name, index=True, header=True, engine="xlsxwriter")

    def batch_write_images_to_disk(self):
        for x in range(len(self.ripple_list)):
            self.ripple_list[x].create_graphic(x,False)



