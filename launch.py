"""
The main program where everything happens-it obtains the data from a csv imported by the user
and then generates the summary and the analysis

"""
from typing import List

from data_acquisition import GetData
from data_analysis import Analyze
from data_display import Display
from data_division import Divide
from data_reconfig import Modify
from database import DatabaseManager
# from data_display import Display
from ripple import Ripple


def main():
    gd = GetData()
    glucose = gd.get_data('titlu_test - Copy.csv')

    d = Divide(glucose)
    trend_list = d.trend_setting()
    threshold = 1
    trend_list_count = d.parting(trend_list, threshold)
    ripple_list = d.generate_ripples(trend_list, trend_list_count)

    # _write_images_to_disk(ripple_list=ripple_list)

    _create_database(divide=d, ripple_list=ripple_list)


def _write_images_to_disk(ripple_list) -> None:
    a = Analyze(ripple_list)

    ripple_connections = a.compare_graphs()
    # time_list = a.compare_duration()

    dis = Display(r_list=ripple_list, ripple_connections=ripple_connections)

    dis.write_summary_to_xls_file()
    dis.write_analysis_to_xls_file()
    dis.batch_write_images_to_disk()


def _create_database(divide: Divide, ripple_list: List[Ripple]) -> None:
    """
    Creates a database of ripples
    """
    db = DatabaseManager("glucose.db")
    data_iter, data_noniter = divide.divide_by_iterable(ripple_list[0])
    db.create_table_if_not_exists("BASIC_DATA_SUMMARY", data_noniter)

    for item in ripple_list:
        data_iter, data_noniter = divide.divide_by_iterable(item)
        _id = db.add("BASIC_DATA_SUMMARY", data_noniter)

        m = Modify()
        simplified_data_iter = m.get_name_and_type(data_iter)

        name_of_individual = f"_BASIC_RAW_DATA_{_id}"
        db.create_table_if_not_exists(name_of_individual, simplified_data_iter)

        for i in range(len(list(data_iter.values())[0])):
            simplified_data_iter_row = m.get_name_and_value(data_iter, i)
            db.add(name_of_individual, simplified_data_iter_row)


if __name__ == "__main__":
    main()
