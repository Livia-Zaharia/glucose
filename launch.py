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
from graph_GUI import Gui
# from data_display import Display
from ripple import Ripple
from pathlib import Path


def main():
    gd = GetData()
    glucose = gd.get_data('titlu_test - Copy.csv')

    d = Divide(glucose)
    trend_list = d.trend_setting()
    threshold = 1
    trend_list_count = d.parting(trend_list, threshold)
    ripple_list = d.generate_ripples(trend_list, trend_list_count)

    p=Path.cwd()
    m = Modify()

    db=_create_basic_database(divide=d, ripple_list=ripple_list, p=p, m=m)
    db_a=_create_analysis_database( ripple_list=ripple_list, p=p, m=m)

    g= Gui(ripple_list,db)
    g.create_viewer()
    # _write_images_to_disk(ripple_list=ripple_list)



def _write_images_to_disk(ripple_list) -> None:
    a = Analyze(ripple_list)

    ripple_connections = a.compare_graphs()
    time_list = a.compare_duration()

    for item in ripple_connections:
        print(len(item),"++++")

    # dis = Display(r_list=ripple_list, ripple_connections=ripple_connections)

    # dis.write_analysis_to_xls_file()
    # dis.batch_write_images_to_disk()


def _create_basic_database(divide: Divide, ripple_list: List[Ripple], p:Path, m:Modify) -> DatabaseManager:
    """
    Creates a database of ripples

    """
    
    if p/"glucose.db" not in p.glob("*"):

        db = DatabaseManager("glucose.db")

        data_iter, data_noniter = divide.divide_by_iterable(ripple_list[0])
        db.create_table_if_not_exists("BASIC_DATA_SUMMARY", data_noniter)

        simplified_data_iter = m.get_name_and_type(data_iter)
        simplified_data_iter.setdefault("ID_ripple",0)

        name_of_individual = "_BASIC_RAW_DATA"
        db.create_table_if_not_exists(name_of_individual, simplified_data_iter)
                
        for item in ripple_list:
            data_iter, data_noniter = divide.divide_by_iterable(item)
            _id = db.add("BASIC_DATA_SUMMARY", data_noniter)

            for i in range(len(list(data_iter.values())[0])):
                simplified_data_iter_row = m.get_name_and_value(data_iter, i)
                simplified_data_iter_row.setdefault("ID_ripple",_id)
                db.add(name_of_individual, simplified_data_iter_row)

        return db
    
    else:
        db = DatabaseManager("glucose.db")
        return db
    
def _create_analysis_database(ripple_list: List[Ripple], p:Path, m:Modify) -> DatabaseManager:
    """
    Creates a database of ripple analysis

    """
    
    if p/"glucose_analysis.db" not in p.glob("*"):

        a = Analyze(ripple_list)

        ripple_connections = a.compare_graphs()
        key_list=["percentage", "From_value", "To_value"]
        ripple_connections_values=[]
        time_list = a.compare_duration()

        for element in ripple_connections:
           for item in element:
               ripple_connections_values.append(item)           

        temp=m.convert_from_tuple_list_to_dict(ripple_connections_values,key_list)


        db = DatabaseManager("glucose_analysis.db")
        simplified_data = m.get_name_and_type(temp)
        
        name_of_individual = "_PATTERN_ANALYSIS_RAW_DATA"
        db.create_table_if_not_exists(name_of_individual, simplified_data)

        for i in range(len(list(temp.values())[0])):
            simplified_data_iter_row = m.get_name_and_value(temp, i)
            db.add(name_of_individual, simplified_data_iter_row)        

        return db
    
    else:
        db = DatabaseManager("glucose_analysis.db")
        return db


if __name__ == "__main__":
    main()
