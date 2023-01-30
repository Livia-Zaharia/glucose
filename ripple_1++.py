
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.io as pio


from datetime import datetime
from matplotlib.dates import date2num


class ripple:

    bg= []
    time_v= []
    trend_v= []

    def add_values(self,bg_value,time_value, trend_value):
        self.bg.append(bg_value)
        self.time_v.append(time_value)
        self.trend_v.append(trend_value)



df=pd.read_csv('titlu_test - Copy.csv', index_col=0)
glucose=df[['Timestamp (YYYY-MM-DDThh:mm:ss)','Glucose Value (mg/dL)']]
#df is from data frame- it extracts a part of a data structure from pandas
#also uses titles to know which column to extract

glucose['Timestamp (YYYY-MM-DDThh:mm:ss)']=pd.to_datetime(glucose['Timestamp (YYYY-MM-DDThh:mm:ss)'])
#convert to format date time from string i guess

glucose['Glucose Value (mg/dL)']=pd.to_numeric(glucose['Glucose Value (mg/dL)'],errors='coerce')
#converts from string to numeric...makes you wonder why they later converted into float
#basically here we have glucose which is a list with headers- like a list of points on a 2D plane

glucose.dropna(inplace=True)  
#dropna= remove nulls

glucose['Glucose Value (mg/dL)']=glucose['Glucose Value (mg/dL)'].astype(float)
glucose= glucose.rename(columns={'Timestamp (YYYY-MM-DDThh:mm:ss)':'Timestamp'})
# converse to float that column and renames timestamp to a less mouthfull name
#all of these come from pandas- to be kept in mind



trend_list =[]
#3 is for the ends of the list
#-2 and 2 are constants in movement- that means is steadly up or down 
# 0 is only for peaks and valley because you can get it only by two opposing signs

trend_list.append(3)

for k in range(1,len(glucose)-1):
    
    a_n=int(glucose.iloc[k,1].astype(int))
    a_n_0=int(glucose.iloc[k-1,1].astype(int))
    a_n_1=int(glucose.iloc[k+1,1].astype(int))

    
    #it is stable that means variation for the whole three numbers is less than 3 in increments
    #this branch in only if the left trend is constant
    # branch for case in which there are two consecutive values in the series
    if a_n==a_n_0:
        a_n_0=int(glucose.iloc[k-2,1].astype(int))
    elif a_n==a_n_1:
        a_n_1=int(glucose.iloc[k+2,1].astype(int))

    
    #this branch is in case it is a growing function
    if a_n_0<a_n:
        temp_trend=1
        if a_n<a_n_1 :
            temp_trend+=1
        else:
            temp_trend+=-1

    #the last branch is in case it decreases
    else:
        temp_trend=-1
        if a_n<a_n_1 :
            temp_trend+=1
        else:
            temp_trend+=-1
    
    trend_list.append(temp_trend)

trend_list.append(3)


#doing some counting- manually
trend_list_index= []
trend_list_count=[]

count=0

for k in range(len(glucose)):

    a_n=trend_list[k]
    count+=1
    if (a_n==0 and count>=50 ):
        trend_list_count.append(count)
        #trend_list_index.append(k)
        count=0

    
#print(trend_list)
#print(trend_list_count)
#print(trend_list_index)

r_list = []

#r_list is a list ready to be filled with ripples
#r_temp is atemporary ripple class object to be added at the end in the previous list

j=0

for x in trend_list_count:
    
    r_temp=ripple ()

    for i in range (j,j+x):

        bg=glucose.iloc[i,1]
        time=glucose.iloc[i,0]
        trend=trend_list[i]
        r_temp.add_values(bg,time,trend)
    r_list.append(r_temp)
    j=x+j


##########################################
##########################################
#the following part just prints out png of the graphs/day-while it is good as script that is not the final intention so 
#we are going to leave it under quotes-if you want to run it before just unquote from the double comments line

# ##########################################
# ##########################################

ending_text="{}c.png"
i=0
j=0
for x in trend_list_count:
    # the syntax x in ....basically will start with first value in gluc_counts- that is 200 something
    #so iloc will start from row 0 to 288 because we are still on the row attribute
    #iloc comes from pandas btw and pandas apparently is built on numpy- who would have thought
    g=glucose.iloc[j:j+x-1]


    fig= px.line(g, x=g['Timestamp'], y=g['Glucose Value (mg/dL)'],range_y=[40,400])
   
    #px here is from plotly express- just to be known- that guy which is recomened to have kaleido installed for
    #kaleido 0.1.*

    fig.update_layout(margin=dict(l=0,r=0,b=0,t=0),xaxis=dict(title=None, visible=False, showgrid=False),yaxis=dict(title=None,ticks="",showticklabels=False,showgrid=False))
   # fig.show()
    fig.write_image(ending_text.format(i))
    #update layout does exactly what it says it does

    j=j+x
    i=i+1
    #only the j moves here, the i is just a counter to write the image

# ##########################################
# ##########################################
