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

"""
Module for a graphical use interface- it allows to generate html files outside the command line
"""


# Function to display a message on the GUI
def write_a_message(text: str):
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


# Function to create a viewer for selecting a Ripple and displaying its graph
def create_viewer(ripple_list: List[Ripple], db: DatabaseManager, ripple_stat_list:List[Ripple_stats]):
    # Define the layout for the viewer window
    layout = [
        [
            [
                sg.Text("Number of element", font=('Arial Bold', 20), expand_x=True, justification='center'),
                sg.In(key="-IN-"),
                sg.Text("                   ",key="-OUT-")
            ],
            [sg.Button("-CREATE ONE-"),
             sg.Button("-CREATE ALL-")
            ]
        ]
    ]

    # Create a window with the defined layout and size
    window = sg.Window("GRAPH_SELECTOR", layout, size=(715, 100))

    while True:
        # Read events and values from the window
        event, values = window.read()
        print(event)
        print("+++++")
        print(values)
        print("*****"*50)

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

            print("before op1")

            window.perform_long_operation(
                lambda: current_ripple.create_graphic(index=index, should_write_html=True,data_path=data_path, slow_insulin=slow_insulin_seq, fast_insulin=fast_insulin_seq),
                '-OPERATION1 DONE-')
            print(window.read())
            print("after op1")
            
            window["-OUT-"].update(f"{index} was written")

            name = data_path / f"_BASIC_RAW_DATA_{index}.xlsx"
            print("before op2")

            window.perform_long_operation(
                lambda: (
                    db.select_and_write_to_xls_file(str(name), "_BASIC_RAW_DATA", {"ID_ripple": str(index)})
                ),
                '-OPERATION2 DONE-'
            )
            print("after op2")

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

                window.perform_long_operation(
                    lambda: current_ripple.create_graphic(index=index, should_write_html=True,data_path=data_path, slow_insulin=slow_insulin_seq, fast_insulin=fast_insulin_seq),
                    '-OPERATION3 DONE-'
                    )
                event,values=window.read()
                # print(window.read())
                # print("after op3")

                # if event == '-OPERATION3 DONE-':
                # window["-OUT-"].update(f"{index} was written")
                name = data_path / f"_BASIC_RAW_DATA_{index}.xlsx"

                window.perform_long_operation(
                    lambda: (
                           db.select_and_write_to_xls_file(str(name), "_BASIC_RAW_DATA", {"ID_ripple": str(index)})
                           ),
                    '-OPERATION4 DONE-'
                    )

                             
            break


    # Close the window
    window.close()


# Function to select a file and return its file path
def select_file() -> str:
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
