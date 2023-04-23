"""
The main program where everything happens-it obtains the data from a csv imported by the user
and then generates the summary and the analysis

"""
import typing as t

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
    
    a = Analyze(ripple_list)
    dis = Display()
    ripple_connections = a.compare_graphs()
    time_list = a.compare_duration()
    
    db_a=_create_analysis_database( ripple_connections, p, m)
    db_a_summary=_extract_summary_of_analysis(ripple_connections, dis)


    g= Gui(ripple_list,db)
    g.create_viewer()

    # dis.batch_write_images_to_disk(ripple_list)

 

def _create_basic_database(divide: Divide, ripple_list: t.List[Ripple], p:Path, m:Modify) -> DatabaseManager:
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
    
def _create_analysis_database(ripple_connections: t.List[t.List[t.Tuple[float,int,int]]], p:Path, m:Modify) -> DatabaseManager:
    """
    Creates a database of ripple analysis

    """
    
    key_list=["percentage", "From_value", "To_value"]
    ripple_connections_values=[]

    for element in ripple_connections:
        for item in element:
            ripple_connections_values.append(item)           

    temp=m.convert_from_tuple_list_to_dict(ripple_connections_values,key_list)
    simplified_data = m.get_name_and_type(temp)
        
    if p/"glucose_analysis.db" not in p.glob("*"):
        
        db = DatabaseManager("glucose_analysis.db")
        name_of_individual = "_PATTERN_ANALYSIS_RAW_DATA"
        db.create_table_if_not_exists(name_of_individual, simplified_data)

        for i in range(len(list(temp.values())[0])):
            simplified_data_iter_row = m.get_name_and_value(temp, i)
            db.add(name_of_individual, simplified_data_iter_row)        

        return db
    
    else:
        db = DatabaseManager("glucose_analysis.db")
        return db

def _extract_summary_of_analysis(ripple_connections: t.List[t.List[t.Tuple[float,int,int]]], dis:Display):
            summary_list = []
            name="graph analysis"

            for item in ripple_connections:
                percent, position_from, position_to = item[-1]
                summary_list.append(f"from {position_from} to {position_to} there is a {round((percent) * 100)}% match")
            
            dis.write_analysis_to_xls_file(summary_list,name)
        

if __name__ == "__main__":
    main()
