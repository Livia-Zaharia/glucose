
import math
import copy
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import plotly.express as px


from datetime import datetime
from matplotlib.dates import date2num


class ripple:

    bg= []
    time_v= []
    trend_v= []
    mean=0.0

    def add_values(self,bg_value,time_value, trend_value):
        self.bg=copy.deepcopy(bg_value)
        self.time_v=copy.deepcopy(time_value)
        self.trend_v=copy.deepcopy(trend_value)


    def average_glucose(self):
        x=0
        count=0

        for elements in self.bg:
            x+=elements
            count+=1
        self.mean=x/count
    

    def print_to_image(self,i:int):
        ending_text="{}c.png"
        
        g=self.bg
        #it is not copied because it is rewritten every time

        fig= px.line(g, x=self.time_v, y=self.bg,range_y=[40,400])
        #px here is from plotly express- just to be known- that guy which is recomened to have kaleido installed for
        #kaleido 0.1.*
        t=list(self.bg).index(max(self.bg))
        print(max(self.bg),"+++++++++++++++++",type(self.bg),"---",len(self.bg) )
        print(self.time_v.iat[t])
        # fig.update_layout(margin=dict(l=0,r=0,b=0,t=0),xaxis=dict(title="Time", visible=True, showgrid=True),yaxis=dict(title="Glucose",ticks="",showticklabels=True,showgrid=True))
        # fig.write_image(ending_text.format(i))

        fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), annotations=[dict(text="MAX", x=self.time_v.iat[t],y=max(self.bg))], xaxis=dict(title="Time", visible=True, showgrid=True),yaxis=dict(title="Glucose",ticks="",showticklabels=True,showgrid=True))
        fig.write_image(ending_text.format(i))
        # fig.add_shape( # add a horizontal "target" line
        # type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",x0=0, x1=len(self.time_v), y0=max(self.bg), y1=max(self.bg))

        # fig.add_annotation( # add a text callout with arrow
        # text="below target!", x="Fri", y=400, arrowhead=1, showarrow=True)

        # update layout does exactly what it says it does



def cvs_insert():
     # the PANDAS region processing

    df=pd.read_csv('titlu_test - Copy.csv', index_col=0)
    
    global glucose
    glucose=df[['Timestamp (YYYY-MM-DDThh:mm:ss)','Glucose Value (mg/dL)']]
    #df is from data frame- it extracts a part of a data structure from pandas
    #also uses titles to know which column to extract

    glucose['Timestamp (YYYY-MM-DDThh:mm:ss)']=pd.to_datetime(glucose['Timestamp (YYYY-MM-DDThh:mm:ss)'])
    #convert to format date time from string read by pandas

    glucose['Glucose Value (mg/dL)']=pd.to_numeric(glucose['Glucose Value (mg/dL)'],errors='coerce')
    #converts from string to numeric...makes you wonder why they later converted into float
    #basically here we have glucose which is a list with headers- like a list of points on a 2D plane

    glucose.dropna(inplace=True)  
    #dropna= remove nulls

    glucose['Glucose Value (mg/dL)']=glucose['Glucose Value (mg/dL)'].astype(float)
    glucose= glucose.rename(columns={'Timestamp (YYYY-MM-DDThh:mm:ss)':'Timestamp'})
    # converse to float that column and renames timestamp to a less mouthful name
    #all of these come from pandas- to be kept in mind



def trend_setting():

    temp_trend_list= []

    for k in range(0,len(glucose)-1):
        a_n=int(glucose.iloc[k,1].astype(int))
        a_n_1=int(glucose.iloc[k+1,1].astype(int))
        
        #iloc[row, column]
        if a_n==a_n_1:
            temp_trend_list.append(0.0)
        else:
            temp_trend_list.append(a_n_1-a_n)
        
    temp_trend_list.append(0.0)
    return temp_trend_list


def parting():
    count=0
    count_positive=0
    count_negative=0
    k=0

    switch=0

    positive_trend=0
    negative_trend=0

    positive_trend_prev=0
    negative_trend_prev=0

    
    while k<len(glucose):
    
        a_n=trend_list[k]
    
        if a_n>=0 and k<len(glucose):
            #print("am dat de pozitive")
            while a_n>=0 and k<len(glucose)-1:
                count_positive+=1
                k+=1
                
                positive_trend+=a_n
                a_n=trend_list[k]
                count+=1
               
            
            positive_trend=positive_trend/count_positive
            switch+=1

        elif a_n<0 and k<len(glucose):
            #print("am dat de negative")
            while a_n<0 and k<len(glucose)-1:
                count_negative+=1
                k+=1
                
                negative_trend+=a_n
                a_n=trend_list[k]
                count+=1
               
            
            negative_trend=negative_trend/count_negative
            negative_trend=negative_trend*(-1)
            switch+=1

        if switch>=2 and count >50:
            
            count_positive=0
            count_negative=0

            if (positive_trend>=threshold and negative_trend>=threshold) or (positive_trend_prev>=threshold and negative_trend>=threshold) or (positive_trend>=threshold and negative_trend_prev>=threshold):
                trend_list_count.append(count)
                count=0
                switch=0
            
            positive_trend_prev=positive_trend
            negative_trend_prev=negative_trend

            positive_trend=0
            negative_trend=0
        
            
        if k==len(glucose) - 1:
                k+=1

def ripple_doing():
    global r_list
    r_list = []

    # #r_list is a list ready to be filled with ripples
    # #r_temp is a temporary ripple class object to be added at the end in the previous list
    j=0
    for x in trend_list_count:
        r_temp=ripple ()

        bg=glucose.iloc[j:j+x,1]
        time=glucose.iloc[j:j+x,0]
        trend=trend_list[j:j+x]
        r_temp.add_values(bg,time,trend)
        r_temp.average_glucose()

        r_list.append(r_temp)

        j=x+j

def main():

    cvs_insert()  

    global trend_list, trend_list_count, threshold
    trend_list =[]
    # we are going to give a positive or negative percentage comparing only two values
    # then when we go to sort we are going to add until we reach 0

    trend_list=trend_setting()
    trend_list_count=[]
    threshold=1


    parting()
    
    ripple_doing()

    for x in range(len(r_list)):
        y=r_list[x].print_to_image(x)



if __name__=="__main__":
    main()