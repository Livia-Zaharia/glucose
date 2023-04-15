"""
The main program where everything happens-it obtains the data from a csv imported by the user
and then generates the summary and the analysis

"""

from database import DatabaseManager
from data_aquisition import GetData
from data_division import Divide
from data_analysis import Analyze
from data_display import Display


def main():


    gd=GetData()
    glucose=gd.csv_insert('titlu_test - Copy.csv')


    d=Divide(glucose)
    trend_list=d.trend_setting()
    threshold=1
    trend_list_count=d.parting(trend_list,threshold)
    r_list=d.ripple_doing(trend_list, trend_list_count)

    a=Analyze(r_list)
    ripple_connections=a.compare_graphs()
    time_list=a.compare_duration()

    """
    The following quoted parts are the direct print to xlsx which are going to be replaced- they work but i want
    to output into a database and then extract from there whatever
    """

    #dis=Display(r_list,ripple_connections)            
    #dis.writing_to_xls_summary()
    #dis.writing_to_xls_analysis()
    #dis.printing_batch_images()

    """
    This part which is not quoted will return some errors at the moment- caused by the timedelta still left
    Also as modification there will be- inclusion of type_for columns only in DB manager
    probably another module to arange the data to be sent to the db or i will change the output of data directly from their corresponding modules
    either way there are some iterations so i am not sure if they are going to remain there
    """

    db=DatabaseManager("glucose.db")

    data_iter,data_noniter=d.divide_by_iterable(r_list[0])
    
    columns=db.type_for_columns(data_noniter)
    db.create_table("BASIC_DATA_SUMMARY",columns)

    for item in r_list:
        data_iter,data_noniter=d.divide_by_iterable(item)
        data_noniter["duration_v"]=str(data_noniter["duration_v"])
        data_noniter["min_t"]=str(data_noniter["min_t"])
        data_noniter["max_t"]=str(data_noniter["max_t"])
        _id=db.add("BASIC_DATA_SUMMARY", data_noniter)

        # will stay commented untill i put a nice method to automatically convert from any datetime object into text so that sqlite reads it


        # simplified_data_iter={}

        # for elem in list(data_iter.keys()):
        #     simplified_data_iter.setdefault(elem,data_iter[elem][0])

        # columns=db.type_for_columns(simplified_data_iter)
        # db.create_table(f"{_id}_BASIC_RAW_DATA",columns)






if __name__=="__main__":
    main()