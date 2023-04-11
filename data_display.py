import copy
from pathlib import Path

import pandas as pd


class Display:
    def __init__(self, r_list, ripple_connections):
        self.r_list = r_list
        self.ripple_connections = ripple_connections

    def writing_to_xls_summary(self):

        file_name = "summary.xlsx"

        p = Path.cwd()
        p = p / file_name

        with pd.ExcelWriter(p, engine="xlsxwriter") as writer:
            for x in range(len(self.r_list)):
                sheet_name = f"{x} summary"
                sheet_name_2 = f"{x} values"
                data = self.r_list[x]

                to_be_processed = copy.deepcopy(dict(vars(data)))
                data_iter = copy.deepcopy(to_be_processed)
                data_noniter = copy.deepcopy(to_be_processed)

                for item in list(to_be_processed.keys()):

                    try:
                        iter(to_be_processed[item])
                    except TypeError:
                        data_iter.pop(item)
                    else:
                        data_noniter.pop(item)

                df = pd.DataFrame(data_noniter, index=[0])
                df['duration_v'] = df['duration_v'].astype(str)

                df.to_excel(writer, sheet_name=sheet_name, header=True, engine="xlsxwriter", index=True)

                df2 = pd.DataFrame.from_dict(data_iter)
                df2.to_excel(writer, sheet_name=sheet_name_2, header=True, engine="xlsxwriter", index=True)

    def writing_to_xls_analysis(self):

        file_name = "analysis.xlsx"

        p = Path.cwd()
        p = p / file_name

        summary_list = []

        with pd.ExcelWriter(p, engine="xlsxwriter") as writer:

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

    def printing_batch_images(self):
        for x in range(len(self.r_list)):
            self.r_list[x].write_image_to_file(x)
