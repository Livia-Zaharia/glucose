import PySimpleGUI as sg
import ripple

# First the window layout in 2 columns

class Gui:
    def __init__(self, ripple_list):
        self.ripple_list=ripple_list
    

    def create_viewer(self):

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
                window.start_thread(lambda: current_ripple.create_graphic(no)  , '-OPERATION DONE-')
            
            elif event == "-OPERATION DONE-":
                window["-OUT-"].update(f"{no} was written")
                
        window.close()