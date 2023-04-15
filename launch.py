"""
The main program where everything happens-it obtains the data from a csv imported by the user
and then generates the summary and the analysis

"""

from data_acquisition import GetData
from data_analysis import Analyze
from data_division import Divide
from database import DatabaseManager


# from data_display import Display


def main():
    gd = GetData()
    glucose = gd.get_data('titlu_test - Copy.csv')

    d = Divide(glucose)
    trend_list = d.trend_setting()
    threshold = 1
    trend_list_count = d.parting(trend_list, threshold)
    ripple_list = d.generate_ripples(trend_list, trend_list_count)

    a = Analyze(ripple_list)
    ripple_connections = a.compare_graphs()
    time_list = a.compare_duration()

    # dis=Display(r_list,ripple_connections)
    # dis.write_summary_to_xls_file()
    # dis.write_analysis_to_xls_file()
    # dis.batch_write_images_to_disk()

    db = DatabaseManager("glucose.db")

    data_iter, data_noniter = d.divide_by_iterable(ripple_list[0])

    columns = db.type_for_columns(data_noniter)
    db.create_table_if_not_exists("BASIC_DATA_SUMMARY", columns)

    for item in ripple_list:
        data_iter, data_noniter = d.divide_by_iterable(item)
        _id = db.add("BASIC_DATA_SUMMARY", data_noniter)

        simplified_data_iter = {}

        for elem in list(data_iter.keys()):
            simplified_data_iter.setdefault(elem, data_iter[elem][0])

        columns = db.type_for_columns(simplified_data_iter)
        db.create_table_if_not_exists(f"{_id}_BASIC_RAW_DATA", columns)


if __name__ == "__main__":
    main()
