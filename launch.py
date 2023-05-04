"""
The main program where everything happens-it obtains the data from a csv imported by the user
and then generates the summary and the analysis

"""
import typing as t
from pathlib import Path

import data_acquisition
import data_display
import data_reconfig
from data_analysis import Analyze
from data_division import Divide
from database import DatabaseManager
from graph_gui import select_file, write_a_message, create_viewer
from ripple import Ripple

CURRENT_PATH_CWD = Path.cwd()
IMAGES_PATH = CURRENT_PATH_CWD / "images_and_graphs"


def main():

    file_location = select_file()

    glucose = data_acquisition.get_glucose_data(file_name=file_location)
    insulin = data_acquisition.get_insulin_data(file_name=file_location)
    write_a_message("FILE ACQUIRED")

    d = Divide(glucose, insulin)
    trend_list = d.trend_setting()

    threshold = 1
    trend_list_count = d.parting(trend_list, threshold)
    ripple_list = d.generate_ripples(trend_list, trend_list_count)
    write_a_message("FILE DIVIDED")

    db = _create_basic_database(divide=d, ripple_list=ripple_list, path=CURRENT_PATH_CWD)
    write_a_message("BASIC DATABASE CREATED")

    a = Analyze(ripple_list=ripple_list)
    
    ripple_connections = a.compare_graphs()
    time_list = a.compare_duration()

    ripple_stat_list=d.generate_ripple_statistics(ripple_list,ripple_connections,time_list)

    for elem in ripple_stat_list[:10]:
        item=vars(elem)
        print (item)
        print("*"*50)
    

    db_a = _create_analysis_database(ripple_connections=ripple_connections, path=CURRENT_PATH_CWD)
    write_a_message("ANALYSIS DATABASE CREATED")

    db_a_summary = _extract_summary_of_analysis(ripple_connections=ripple_connections)
    write_a_message("SUMMARY OF ANALYSIS CREATED")

    create_viewer(ripple_list, db, ripple_stat_list)

    # data_display.batch_write_graphs_to_disk(ripple_list=ripple_list, base_path=IMAGES_PATH)


def _create_basic_database(divide: Divide, ripple_list: t.List[Ripple], path: Path) -> DatabaseManager:
    """
    Creates a database of ripples

    """

    if path / "glucose.db" not in path.glob("*"):

        db = DatabaseManager("glucose.db")

        data_dict, data_noniter = divide.divide_by_iterable(data=ripple_list[0])
        db.create_table_if_not_exists("BASIC_DATA_SUMMARY", data_noniter)

        simplified_data_iter = data_reconfig.get_name_and_type(data_dict=data_dict)
        simplified_data_iter.setdefault("ID_ripple", 0)

        name_of_individual = "_BASIC_RAW_DATA"
        db.create_table_if_not_exists(name_of_individual, simplified_data_iter)

        for item in ripple_list:
            data_dict, data_noniter = divide.divide_by_iterable(data=item)
            _id = db.add("BASIC_DATA_SUMMARY", data_noniter)

            for index in range(len(list(data_dict.values())[0])):
                simplified_data_iter_row = data_reconfig.get_name_and_value(data_iter=data_dict, index=index)
                simplified_data_iter_row.setdefault("ID_ripple", _id)
                db.add(name_of_individual, simplified_data_iter_row)

        return db

    else:
        db = DatabaseManager("glucose.db")
        return db


def _create_analysis_database(ripple_connections: t.List[t.List[t.Tuple[float, int, int]]], path: Path) \
        -> DatabaseManager:
    """
    Creates a database of ripple analysis

    """

    key_list = ["percentage", "From_value", "To_value"]
    ripple_connections_values = []

    for element in ripple_connections:
        for item in element:
            ripple_connections_values.append(item)

    temp = data_reconfig.convert_from_tuple_list_to_dict(input_list=ripple_connections_values, key_list=key_list)
    simplified_data = data_reconfig.get_name_and_type(temp)

    if path / "glucose_analysis.db" not in path.glob("*"):

        db = DatabaseManager("glucose_analysis.db")
        name_of_individual = "_PATTERN_ANALYSIS_RAW_DATA"
        db.create_table_if_not_exists(name_of_individual, simplified_data)

        for index in range(len(list(temp.values())[0])):
            simplified_data_iter_row = data_reconfig.get_name_and_value(data_iter=temp, index=index)
            db.add(name_of_individual, simplified_data_iter_row)

        return db

    else:
        db = DatabaseManager("glucose_analysis.db")
        return db


def _extract_summary_of_analysis(ripple_connections: t.List[t.List[t.Tuple[float, int, int]]]):
    summary_list = []
    sheet_name = "graph analysis"

    for item in ripple_connections:
        percent, position_from, position_to = item[-1]
        summary_list.append(f"from {position_from} to {position_to} there is a {round((percent) * 100)}% match")

    data_display.write_analysis_to_xls_file(summary_list=summary_list, sheet_name=sheet_name)


if __name__ == "__main__":
    main()
