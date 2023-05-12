"""
The main program where everything happens-it obtains the data from a csv imported by the user
and then generates the summary and the analysis
"""
import typing as t
from pathlib import Path
from copy import deepcopy

import data_acquisition
import data_display
import data_reconfig
import constants
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

    d = Divide(glucose=glucose, insulin=insulin)
    start_end=d.interval()
    trend_list = d.trend_setting()

    threshold = 1
    trend_list_count = d.parting(trend_list, threshold)
    ripple_list = d.generate_ripples(trend_list, trend_list_count)
    write_a_message("FILE DIVIDED")

    db = _create_basic_database(divide=d, ripple_list=ripple_list, path=CURRENT_PATH_CWD, start_end=start_end)
    write_a_message("BASIC DATABASE CREATED")

    a = Analyze(ripple_list=ripple_list)
    
    ripple_connections = a.compare_graphs()

    ripple_stat_list=d.generate_ripple_statistics(ripple_list,ripple_connections)

    # for elem in ripple_stat_list:
    #     item=vars(elem)
    #     for item0 in item:
    #         print (item0)
    #         print("-----------")
    #         print (type(item0))
    #     print("*"*50)
    

    db_a = _create_analysis_database(ripple_connections=ripple_connections, path=CURRENT_PATH_CWD)
    write_a_message("ANALYSIS DATABASE CREATED")

    _extract_summary_of_analysis(ripple_connections=ripple_connections)
    write_a_message("SUMMARY OF ANALYSIS CREATED")

    db_s=_create_stat_database(ripple_stat_list=ripple_stat_list, path=CURRENT_PATH_CWD)
    write_a_message("STATISTIC DATABASE CREATED")

    create_viewer(ripple_list, db, ripple_stat_list, db_s, db_a)



def _create_basic_database(divide: Divide, ripple_list: t.List[Ripple], path: Path,start_end:str) -> DatabaseManager:
    """
    Creates a database of ripples

    Args:
        divide: A Divide object containing methods for division
        ripple_list: a list of ripple objects
        path: the path where to save the database
        start_end: str representing the time interval timestamp value for the file

    Returns:
        db:DatabaseManager object containing the glucose data

    """

    db_new_name=constants.GLUCOSE_DB+start_end+".db"
    print(db_new_name)
    print (type(db_new_name))
    #check if there is a database in that location already
    if path / db_new_name not in path.glob("*"):

        db = DatabaseManager(db_new_name)

        #split the ripple into iterable and not iterable dictionaries 
        data_dict, data_noniter = divide.divide_by_iterable(data=ripple_list[0])
        #creates the table of non iterable items
        db.create_table_if_not_exists("BASIC_DATA_SUMMARY", data_noniter)
        print (data_dict)
        print(data_noniter)

        #creates a new dict containing the same key but with values that are the 
        # type of each list's composing items

        data_dict=data_reconfig.convert_to_list(data_dict)

        simplified_data_iter = data_reconfig.get_name_and_type(data_dict=data_dict)
        simplified_data_iter.setdefault("ID_ripple", 0)

        #creates the table for iterable items
        name_of_individual = "_BASIC_RAW_DATA"
        db.create_table_if_not_exists(name_of_individual, simplified_data_iter)

        #takes each item in ripple list, divides it into iterable and not iterable
        for item in ripple_list:
            data_iter, data_noniter = divide.divide_by_iterable(data=item)
            #extracts position of ripple in list (index from list)
            _id = db.add("BASIC_DATA_SUMMARY", data_noniter)

            #writes line per line the iterable values found in the ripple element at given index
            for index in range(len(list(data_iter.values())[0])):
                data_iter=data_reconfig.convert_to_list(data_iter)
                simplified_data_iter_row = data_reconfig.get_name_and_value(data_iter=data_iter, index=index)
                simplified_data_iter_row.setdefault("ID_ripple", _id)
                db.add(name_of_individual, simplified_data_iter_row)

        return db

    else:
        db = DatabaseManager(db_new_name)
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

def _create_stat_database(ripple_stat_list, path):
    
    
    if path / "glucose_statistic.db" not in path.glob("*"):

        db = DatabaseManager("glucose_statistic.db")

        data = deepcopy(dict(vars(ripple_stat_list[0])))
        data["slow_insulin_seq"]=data_reconfig.convert_list_of_tuples_to_string(data["slow_insulin_seq"])
        data["fast_insulin_seq"]=data_reconfig.convert_list_of_tuples_to_string(data["fast_insulin_seq"])
        db.create_table_if_not_exists("_GLUCOSE_STATS", data)


        for no,item in enumerate(ripple_stat_list):
            data_noniter = deepcopy(dict(vars(item)))
            data_noniter["slow_insulin_seq"]=data_reconfig.convert_list_of_tuples_to_string(data_noniter["slow_insulin_seq"])
            data_noniter["fast_insulin_seq"]=data_reconfig.convert_list_of_tuples_to_string(data_noniter["fast_insulin_seq"])
            _id = db.add("_GLUCOSE_STATS", data_noniter)

        return db

    else:
        db = DatabaseManager("glucose_statistic.db")
        return db


if __name__ == "__main__":
    main()
