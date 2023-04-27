from pathlib import Path
from typing import List

import PySimpleGUI as sg

from database import DatabaseManager
from ripple import Ripple

CURRENT_PATH_CWD = Path.cwd()
IMAGES_PATH = CURRENT_PATH_CWD / "images_and_graphs"

"""
Module for a graphical use interface- it allows to generate html files outside the command line

"""


def write_a_message(text: str):
    layout = [[sg.Text(text, font=('Arial Bold', 20), expand_x=True, justification='center')], ]
    window = sg.Window('File processing', layout, size=(715, 100))

    while True:
        event, values = window.read(timeout=5000)

        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == sg.TIMEOUT_KEY:
            break

    window.close()


def create_viewer(ripple_list: List[Ripple], db: DatabaseManager):
    """
    Method of the GUI- at the moment it allows the user to input a
    number, and then it generates the html file by using the method from the ripple class

    """
    layout = [
        [
            [
                sg.Text("Number of element", font=('Arial Bold', 20), expand_x=True, justification='center'),
                sg.In(key="-IN-"),
                sg.Text(key="-OUT-")
            ],
            sg.Button("Go")
        ]
    ]

    window = sg.Window("GRAPH_SELECTOR", layout, size=(715, 100))

    while True:
        event, values = window.read()

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        # no = 0

        if event == "Go":
            no = int(values["-IN-"])
            current_ripple = ripple_list[no]
            window.start_thread(lambda: current_ripple.create_graphic(no, True), '-OPERATION1 DONE-')

        elif event == "-OPERATION1 DONE-":
            window["-OUT-"].update(f"{no} was written")

            data_path = IMAGES_PATH / f"Ripple_no{no}"
            data_path.mkdir(parents=True, exist_ok=True)
            name = data_path / f"_BASIC_RAW_DATA_{no}.xlsx"

            window.start_thread(
                lambda: (
                    db.select_and_write_to_xls_file(name, "_BASIC_RAW_DATA", {"ID_ripple": str(no)})
                ),
                '-OPERATION2 DONE-'
            )

    window.close()


def select_file() -> str:
    """
    method that allows user to select file and get the file path

    """
    layout = [
        [sg.Text('Select a file', font=('Arial Bold', 20), expand_x=True, justification='center')],
        [
            sg.Input(enable_events=True, key='-IN-', font=('Arial Bold', 12), expand_x=True),
            sg.FileBrowse("select")
        ]
    ]
    window = sg.Window('Select file', layout, size=(715, 100))

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == '-IN-':
            a = values["select"]
            break

    window.close()

    return a
