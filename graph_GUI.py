import PySimpleGUI as sg
from ripple import Ripple
from typing import List

"""
Module for a graphical use interface- it allows to generate html files outside the command line

"""

class Gui:
    """
    Class that has the GUI viewer defined

    """
    def __init__(self, ripple_list:List[Ripple]):
        self.ripple_list=ripple_list
    
    def create_viewer(self):
        """
        Method of the GUI- at the moment it allows the user to input a 
        number and then it generates the html file by using the method from the ripple class
        
        """

        column = [
            [
                sg.Text("Number of element"),
                sg.In(key="-IN-"),
                sg.Text(key="-OUT-")
            ],
        ]


        layout = [
            [
                sg.Column(column),
                sg.Button("Go")
            ]
        ]

        window = sg.Window("GRAPH_SELECTER", layout)

        
        while True:
            event, values = window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break                
                
            if event == "Go":
                no=int(values["-IN-"])
                current_ripple=self.ripple_list[no]
                window.start_thread(lambda: current_ripple.create_graphic(no,True)  , '-OPERATION DONE-')
            
            elif event == "-OPERATION DONE-":
                window["-OUT-"].update(f"{no} was written")
                
        window.close()