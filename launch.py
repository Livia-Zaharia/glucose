"""
The main program where everything happens-it obtains the data from a csv imported by the user
and then generates the summary and the analysis

"""

import pandas as pd
# import database
from ripple import Ripple
from data_aquisition import GetData
from data_division import Divide
from data_analisys import Analyze
from data_display import Display


def main():


    gd=GetData()
    glucose=gd.cvs_insert('titlu_test - Copy.csv')


    d=Divide(glucose)
    trend_list=d.trend_setting()
    threshold=1
    trend_list_count=d.parting(trend_list,threshold)
    r_list=d.ripple_doing(trend_list, trend_list_count)

    a=Analyze(r_list)
    ripple_connections=a.compare_graphs()
    time_list=a.compare_duration()

    dis=Display(r_list,ripple_connections)            
    dis.writing_to_xls_summary()
    dis.writing_to_xls_analysis()
    dis.printing_batch_images()




if __name__=="__main__":
    main()