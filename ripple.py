"""
The module for object Ripple. Has all the methods and values of it
"""

import copy
from pathlib import Path
import pandas as pd
import plotly.express as px
CURRENT_PATH_CWD = Path.cwd()
IMAGES_PATH = CURRENT_PATH_CWD / "images_and_graphs"


class Ripple:
    """
    Object Ripple is a class that stores the blood glucose values from the csv, together with additional info. The
    way it is defined, a Ripple object will contain only ONE  change of sign of the graph-simply put one change from
    an ascending part to descending part or vice versa. For more information see definition of add_values method.(
    bg=dataframe slice type-int values| time_v= dataframe slice type-datetime values| trend_v=float list type|
    normalized_graph=float list type| mean= single float value| start_t=datetime| end_t=datetime| duration_v= timedelta type| min_v=int type| min_t=
    timedate type| min_index= int type| max_v=int type| max_t= timedate type| max_index= int type)

    """

    def __init__(self):
        self.bg = pd.DataFrame()
        self.time_v = pd.DataFrame()
        self.trend_v = []
        self.normalized_graph = []
        self.mean = 0.0
        self.start_t=0
        self.end_t=0
        self.duration_v = 0.0
        self.min_v = 0.0
        self.min_t = 0.0
        self.min_index = 0
        self.max_v = 0.0
        self.max_t = 0.0
        self.max_index = 0

    def add_values(self, bg_value: pd.DataFrame, time_value: pd.DataFrame, trend_value: list) -> None:
        """
        Method for initializing the class. Runs the methods (duration()| average_glucose()| min_max_value_time()|
        normalizing()) bg_value: is a slice from a DataFrame- it extracts only the column with blood glucose values|
        time_value: slice from DataFrame- it extracts the timedate for the previous extracted blood glucose|
        trend_value: standard list containing the differences in values between the current number (the one that
        gives the index value) and the previous one

        """
        self.bg = copy.deepcopy(bg_value)
        self.time_v = copy.deepcopy(time_value)
        self.trend_v = copy.deepcopy(trend_value)

        self._inner_init()

    def _inner_init(self) -> None:
        self._make_duration()
        self._make_average_glucose()
        self._get_min_max_value_time()
        self._normalize_graph()

    def _make_duration(self) -> None:
        """
        Method for extracting the total time duration of a ripple object. As both start and end date are timedate
        objects the result is timedelta. self.duration=timedelta type

        """
        self.start_t=self.time_v.iat[0]
        self.end_t=self.time_v.iat[len(self.time_v) - 1]
        self.duration_v = self.end_t - self.start_t

    def _make_average_glucose(self) -> None:
        """
        Method for obtaining the mean value of all the bloodglucose values in this period of time.
        self.mean=float type
        
        """
        x = 0
        count = 0

        for elements in self.bg:
            x += elements
            count += 1

        self.mean = round(x / count, 2)

    def _get_min_max_value_time(self) -> None:
        """
        Method for obtaining the min and max value, time and index in the DataFrame slice.
        (self.min_v=int type| self.min_t= timedate type| self.min_index= int type|
         self.max_v=int type| self.max_t= timedate type| self.max_index= int type)

        """

        self.min_v = min(self.bg)
        self.max_v = max(self.bg)

        self.max_index = list(self.bg).index(self.max_v)
        self.min_index = list(self.bg).index(self.min_v)

        self.max_t = self.time_v.iat[self.max_index]
        self.min_t = self.time_v.iat[self.min_index]

    def _normalize_graph(self) -> None:
        """
        Method for normalizing the graph. Basically it defines a list as long as the DataFrame slice with float
        values going from (0,1]. self.normalized_graph= float list type

        """
        temp_normalized_graph = []

        for item in list(self.bg):
            temp_normalized_graph.append(round(item / self.max_v, 2))

        self.normalized_graph = copy.deepcopy(temp_normalized_graph)

    def _compile_legend(self) -> str:
        """
        Method for compiling a basic str for legend display.
        
        """

        legend_0 = "amplitude=" + str(self.max_v - self.min_v) + '<br>'
        legend_0 += "average value=" + str(self.mean) + "mg/dL" + '<br>'
        legend_0 += "duration=" + str(self.duration_v) + '<br>'

        legend_0 += "start time=" + str(self.time_v.iat[0]) + '<br>'
        legend_0 += "end time=" + str(self.time_v.iat[len(self.time_v) - 1]) + '<br>'

        legend_0 += "min=" + str(self.min_v) + "mg/dL" + '<br>'
        legend_0 += "min_time@=" + str(self.min_t) + '<br>'
        legend_0 += "max=" + str(self.max_v) + "mg/dL" + '<br>'
        legend_0 += "max_time@=" + str(self.max_t) + '<br>'

        return legend_0

    def create_graphic(self, i: int, flag: bool) -> None:
        """
        Method of ripple class to produce a graphic in a browser and then save as a html or png of the 
        ripple with the legend. Made using plotly express
        i value is the position, flag value- True outputs html, False -outputs png directly
        
        """
        DATA_PATH=IMAGES_PATH/f"Ripple_no{i}"
        DATA_PATH.mkdir(parents=True,exist_ok=True)
        
        g = self.bg

        legend_values = self._compile_legend()

        fig = px.line(g, x=self.time_v, y=self.bg, range_y=[40, 400])

        fig.add_hline(max(self.bg), line_width=1, line_dash="dash")
        fig.add_hline(min(self.bg), line_width=1, line_dash="dash")
        fig.add_annotation(text="MIN", x=self.min_t, y=self.min_v)
        fig.add_annotation(text="MAX", x=self.max_t, y=self.max_v)

        fig.add_vline(self.time_v.iat[len(self.time_v) - 1], line_width=1, line_dash="dash")

        fig.add_annotation(text=legend_values, x=self.time_v.iat[len(self.time_v) - 1], y=300, xanchor="left",
                           font=dict(family="Arial", size=11))

        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), xaxis=dict(title="Time", visible=True, showgrid=True),
                          yaxis=dict(title="Glucose", ticks="", showticklabels=True, showgrid=True))
        if flag == True:
            ending_text = DATA_PATH/f"images{i}.html"
            fig.write_html(ending_text)
        else:
            ending_text = DATA_PATH/f"images{i}.png"
            fig.write_image(ending_text)
