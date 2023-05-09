"""
Module for a graphical use interface- it allows to generate html files outside the command line
"""

from pathlib import Path
from typing import List

import PySimpleGUI as sg

from database import DatabaseManager
from ripple import Ripple
from data_statistic import Ripple_stats

# Set the current working directory path
CURRENT_PATH_CWD = Path.cwd()
# Set the image's path inside the current working directory
IMAGES_PATH = CURRENT_PATH_CWD / "images_and_graphs"


def write_a_message(text: str) ->None:
    """
    Function to display a message on the GUI

    Args:
        text:str value to show
    """
    
    # Define the layout for the message window
    layout = [[sg.Text(text, font=('Arial Bold', 20), expand_x=True, justification='center')], ]
    # Create a window with the defined layout and size
    window = sg.Window('File processing', layout, size=(715, 100))

    while True:
        # Read events and values from the window
        event, values = window.read(timeout=3000)

        # If the event is "Exit" or the window is closed, break the loop
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        # If the event is a timeout, break the loop
        if event == sg.TIMEOUT_KEY:
            break

    # Close the window
    window.close()

def create_viewer(ripple_list: List[Ripple], db: DatabaseManager, ripple_stat_list:List[Ripple_stats], db_s:DatabaseManager, db_a:DatabaseManager) -> None:
    """
    Function to create a viewer for selecting a Ripple and displaying its graph

    Args:
        ripple_list: the ripple list that contains all the Ripple objects in the sequence
                    it will be used to extract the html version of the graph
        db:the DatabaseManager object that contains the glucose basic raw data
                    it will be used to extract the xls version of the data summary
        ripple_stat_list: the list that contains the Ripple_Stats objects for each Ripple in part
                    it will be used to extract the insulin data position
    """
    # Define the layout for the viewer window
    layout = [
        [
            [
                sg.Text("Number of element", font=('Arial Bold', 20), expand_x=True, justification='center', grab= True),
                sg.In(key="-IN-"),
                sg.Text("                    ",key="-OUT-")
            ],

            [
               sg.Rad(text="HTML",group_id=1,key="-HTML-"),
               sg.Rad(text="XLS raw data",group_id=1, key="-XLS RAW-"),
               sg.Rad(text="XLS analysis",group_id=1, key="-XLS ANALYSIS-"),
               sg.Rad(text="ALL",group_id=1, key="-EXTRACT ALL-") 
            ],
            
            [
                sg.Button("-CREATE ONE-"),
                sg.Button("-CREATE ALL-")
            ]
            
        ]
    ]

    # Create a window with the defined layout and size
    window = sg.Window("GRAPH_SELECTOR", layout,size =(800,150))
    

    while True:
        # Read events and values from the window
        event, values = window.read()

        # If the event is "Exit" or the window is closed, break the loop
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        # If the event is "-CREATE ONE-", create the graphic and the excel for the selected Ripple
        if event == "-CREATE ONE-":
            
            index = int(values["-IN-"])
            current_ripple = ripple_list[index]
            current_ripple_stat=ripple_stat_list[index]
            slow_insulin_seq=current_ripple_stat.slow_insulin_seq
            fast_insulin_seq=current_ripple_stat.fast_insulin_seq

                
            data_path = IMAGES_PATH / f"Ripple_no{index}"
            data_path.mkdir(parents=True, exist_ok=True)

            if values["-EXTRACT ALL-"] or values["-HTML-"]:

                window.perform_long_operation(
                    lambda: current_ripple.create_graphic(index=index, should_write_html=True,data_path=data_path, 
                                                        slow_insulin=slow_insulin_seq, fast_insulin=fast_insulin_seq),
                                            '-ONE HTML DONE-')
            
            if values["-EXTRACT ALL-"] or values["-XLS RAW-"]:

                name = data_path / f"_01_BASIC_DATA_{index}.xlsx"
                
                window.perform_long_operation(
                    lambda: (db.select_and_write_to_xls_file(name=str(name), table_name="BASIC_DATA_SUMMARY", sheet_name="BASIC DATA SUMMARY", criteria={"ID": str(index)})),
                                            '-ONE XLS BASIC DONE-')
                

                name = data_path / f"_02_BASIC_RAW_DATA_{index}.xlsx"

                window.perform_long_operation(
                    lambda: (db.select_and_write_to_xls_file(name=str(name), table_name="_BASIC_RAW_DATA", criteria={"ID_ripple": str(index)})),
                                            '-ONE XLS RAW DONE-')
            

            if values["-EXTRACT ALL-"] or values["-XLS ANALYSIS-"]:
                                             
                name = data_path / f"_03_GLUCOSE STATS_{index}.xlsx"

                window.perform_long_operation(
                            lambda: (db_s.select_and_write_to_xls_file(name=str(name), table_name="_GLUCOSE_STATS", sheet_name="GLUCOSE STATS", criteria={"ID": str(index)})),
                                                '-ONE XLS GLUCOSE STATS DONE-')
                
                name = data_path / f"_04_ANALYSIS_DATA_RAW_{index}.xlsx"
                
                window.perform_long_operation(
                    lambda: (db_a.select_and_write_to_xls_file(name=str(name), table_name="_PATTERN_ANALYSIS_RAW_DATA", sheet_name="PATTERN RAW DATA", criteria={"From_value": str(index)})),
                                            '-ONE XLS ANALYSIS DONE-')
           

           
            window["-OUT-"].update(f"{index} was written")



        # If the event is "-CREATE ALL-", create the graphic and the excel for ALL the Ripples
        #use perform_long_operation rather than start thread since perform long operation also closes the thread
       
        if event == "-CREATE ALL-":

            for index in range (len(ripple_list)):
                current_ripple = ripple_list[index]
                current_ripple_stat=ripple_stat_list[index]
                slow_insulin_seq=current_ripple_stat.slow_insulin_seq
                fast_insulin_seq=current_ripple_stat.fast_insulin_seq

            
                data_path = IMAGES_PATH / f"Ripple_no{index}"
                data_path.mkdir(parents=True, exist_ok=True)

                if values["-EXTRACT ALL-"] or values["-HTML-"]:

                    window.perform_long_operation(
                        lambda: current_ripple.create_graphic(index=index, should_write_html=True,data_path=data_path, 
                                                            slow_insulin=slow_insulin_seq, fast_insulin=fast_insulin_seq),
                                                '-ALL HTML DONE-')
                                    
                    event,values=window.read()
                
                if values["-EXTRACT ALL-"] or values["-XLS RAW-"]:

                    name = data_path / f"_01_BASIC_DATA_{index}.xlsx"
                
                    window.perform_long_operation(
                        lambda: (db.select_and_write_to_xls_file(name=str(name), table_name="BASIC_DATA_SUMMARY", sheet_name="BASIC DATA SUMMARY", criteria={"ID": str(index)})),
                                            '-ALL XLS BASIC DONE-')
                    
                    event,values=window.read()
                    name = data_path / f"_02_BASIC_RAW_DATA_{index}.xlsx"

                    window.perform_long_operation(
                        lambda: (db.select_and_write_to_xls_file(name=str(name), table_name="_BASIC_RAW_DATA", criteria={"ID_ripple": str(index)})),
                                            '-ALL XLS RAW DONE-')
                    event,values=window.read()
                    

                if values["-EXTRACT ALL-"] or values["-XLS ANALYSIS-"]:
                                             
                    name = data_path / f"_03_GLUCOSE STATS_{index}.xlsx"

                    window.perform_long_operation(
                            lambda: (db_s.select_and_write_to_xls_file(name=str(name), table_name="_GLUCOSE_STATS", sheet_name="GLUCOSE STATS", criteria={"ID": str(index)})),
                                                '-ALL XLS GLUCOSE STATS DONE-')
                
                    event,values=window.read()
                    name = data_path / f"_04_ANALYSIS_DATA_RAW_{index}.xlsx"
                
                    window.perform_long_operation(
                        lambda: (db_a.select_and_write_to_xls_file(name=str(name), table_name="_PATTERN_ANALYSIS_RAW_DATA", sheet_name="PATTERN RAW DATA", criteria={"From_value": str(index)})),
                                            '-ALL XLS ANALYSIS DONE-')
                    event,values=window.read()
                    
               

            break


    # Close the window
    window.close()

def select_file() -> str:
    """
    Function to select a file and return its file path    
    """
    # Define the layout for the file selection window
    layout = [
        [sg.Text('Select a csv file', font=('Arial Bold', 20), expand_x=True, justification='center')],
        [
            sg.Input(enable_events=True, key='-IN-', font=('Arial Bold', 12), expand_x=True),
            sg.FileBrowse("select",file_types=(("CSV files","*.csv"),))
        ]
    ]
    # Create a window with the defined layout and size
    window = sg.Window('Select file', layout, size=(715, 100))

    # Define the file path as Not Available
    file_path_str = 'N/A'

    # Read events in loop
    while True:
        # Read events and values from the window
        event, values = window.read()

        # If the event is "Exit" or the window is closed, break the loop
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        # If the event is the input event, store the selected file path in variable 'a'
        if event == '-IN-':
            file_path_str = values["select"]
            break

    # Close the window
    window.close()

    # Return the selected file path
    return file_path_str
