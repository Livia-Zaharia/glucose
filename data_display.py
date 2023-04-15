from pathlib import Path

import pandas as pd

from constants import SUMMARY_XLSX_FILE_NAME, ANALYSIS_XLSX_FILE_NAME
from data_division import Divide

CURRENT_PATH_CWD = Path.cwd()


class Display:
    def __init__(self, r_list, ripple_connections):
        self.ripple_list = r_list
        self.ripple_connections = ripple_connections

    def write_summary_to_xls_file(self):
        with pd.ExcelWriter(CURRENT_PATH_CWD / SUMMARY_XLSX_FILE_NAME, engine="xlsxwriter") as writer:
            for index in range(len(self.ripple_list)):
                sheet_name = f"{index} summary"
                sheet_name_2 = f"{index} values"
                ripple_data = self.ripple_list[index]

                div = Divide()
                data_iter, data_noniter = div.divide_by_iterable(ripple_data)

                df = pd.DataFrame(data_noniter, index=[0])
                df['duration_v'] = df['duration_v'].astype(str)

                df.to_excel(writer, sheet_name=sheet_name, header=True, engine="xlsxwriter", index=True)

                df2 = pd.DataFrame.from_dict(data_iter)
                df2.to_excel(writer, sheet_name=sheet_name_2, header=True, engine="xlsxwriter", index=True)

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
            self.ripple_list[x].write_to_image_file(x)
