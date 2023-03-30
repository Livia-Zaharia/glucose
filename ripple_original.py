
import math
import copy
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import plotly.express as px
from datetime import datetime
from matplotlib.dates import date2num
from pathlib import Path


class ripple:

    bg= []
    time_v= []
    trend_v= []
    normalized_graph=[]
    mean=0.0
    duration_v=0.0
    min_v=0.0
    min_t=0.0
    min_index=0
    max_v=0.0
    max_t=0.0
    max_index=0

    def add_values(self,bg_value,time_value, trend_value):
        self.bg=copy.deepcopy(bg_value)
        self.time_v=copy.deepcopy(time_value)
        self.trend_v=copy.deepcopy(trend_value)

        self.duration()
        self.average_glucose()
        self.min_max_value_time()
        self.normalizing()

    def duration(self):
        self.duration_v=self.time_v.iat[len(self.time_v)-1]-self.time_v.iat[0]
 
    def average_glucose(self):
        x=0
        count=0

        for elements in self.bg:
            x+=elements
            count+=1
        self.mean=round(x/count,2)

    def min_max_value_time(self):
        self.min_v=min(self.bg)
        self.max_v=max(self.bg)

        self.max_index=list(self.bg).index(self.max_v)
        self.min_index=list(self.bg).index(self.min_v)

        self.max_t=self.time_v.iat[self.max_index]
        self.min_t=self.time_v.iat[self.min_index]

    def normalizing(self):
        temp_normalized_graph=[]
        for item in list(self.bg):
            temp_normalized_graph.append(round(item/self.max_v,2))
        self.normalized_graph=copy.deepcopy(temp_normalized_graph)

    def legend_compiling(self):
        legend_0="amplitude="+str(self.max_v-self.min_v)+'<br>'
        legend_0+="average value="+str(self.mean)+"mg/dL"+'<br>'
        legend_0+="duration="+str(self.duration_v)+'<br>'

        legend_0+="start time="+str(self.time_v.iat[0])+'<br>'
        legend_0+="end time="+str(self.time_v.iat[len(self.time_v)-1])+'<br>'
        
        
        legend_0+="min="+str(self.min_v)+"mg/dL"+'<br>'
        legend_0+="min_time@="+str(self.min_t)+'<br>'
        legend_0+="max="+str(self.max_v)+"mg/dL"+'<br>'
        legend_0+="max_time@="+str(self.max_t)+'<br>'
       
        return legend_0

    def print_to_image(self,i:int):
        ending_text="{}.png"
        g=self.bg
        #it is not copied because it is rewritten every time

        legend_values=self.legend_compiling()


        fig= px.line(g, x=self.time_v, y=self.bg,range_y=[40,400])

        fig.add_hline(max(self.bg), line_width=1, line_dash="dash")
        fig.add_hline(min(self.bg), line_width=1, line_dash="dash")
        fig.add_annotation(text="MIN", x=self.min_t,y=self.min_v)
        fig.add_annotation(text="MAX", x=self.max_t,y=self.max_v)

        fig.add_vline(self.time_v.iat[len(self.time_v)-1], line_width=1, line_dash="dash")

        fig.add_annotation(text=legend_values, x=self.time_v.iat[len(self.time_v)-1],y=300, xanchor="left",font=dict(family="Arial", size=11))
    

        fig.update_layout(margin=dict(l=0,r=0,b=0,t=0), xaxis=dict(title="Time", visible=True, showgrid=True),yaxis=dict(title="Glucose",ticks="",showticklabels=True,showgrid=True))
        fig.write_image(ending_text.format(i))




def round_to_multiple(number,multiple):
    return multiple*round(number/multiple)

def cvs_insert():
    # the PANDAS region processing
    p=Path.cwd()
    file_name='titlu_test - Copy.csv'
    p=p/file_name

    df=pd.read_csv(p, index_col=0)

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

    """"
    so basically we go like this- we run the trend list- then we check what kind of trend we hve- positive or negative and we run on it 
    until you can't run no more. we keep track of the previous run - if we changed sign at least once- that is switch is bigger than 2 and we have at
    least 50 values- to avoid values like+1,-1,+2,-1- and positive and negative trends have at least 1 item - then we can proceed to split
    we have to build trend list count list- where we find out how many items are per slice
    """
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

        r_list.append(r_temp)

        j=x+j

def analize():
    compare_graphs()
    compare_duration()

def compare_graphs():
    global ripple_connections
    ripple_connections=[]

    for item in r_list:
        ripple_connections.append([])

    """
    create the empty list with lists/item in which we are going to load tuples
    """    
    
    for search_item in r_list:
        for compare_item in r_list[r_list.index(search_item)+1:]:
            
            percent_search_value=0
            percent_compare_value=0

            common_interval,isclose_values=compare_two_graphs(search_item, compare_item)
            
            if isclose_values!=0:
                percent_search_value=round(isclose_values/len(search_item.normalized_graph),2)
                percent_compare_value=round(isclose_values/len(compare_item.normalized_graph),2)
                ripple_connections[r_list.index(search_item)].append((percent_search_value,r_list.index(search_item),r_list.index(compare_item)))
                ripple_connections[r_list.index(compare_item)].append((percent_compare_value,r_list.index(compare_item),r_list.index(search_item)))
            

            """here should be the is close method- we update the graph connection both ways that is why we search only going fwd"
            also we recieve lenght of overlapping and how many are coresponding"""
        
    
    for item in ripple_connections:
        item.sort()

def compare_duration():
    time_list=[]
    for item in r_list:
        time=item.duration_v.total_seconds()
        time=round_to_multiple(time,3600)
        time_list.append(time/3600)
    
    time_list.sort()
    time_list=set(time_list)
    time_list=list(time_list)
    

def compare_two_graphs(A:ripple, B:ripple)->tuple:
    
    start_A_index=0
    start_B_index=0
    
    flag=0

    max_A_index=A.max_index
    max_B_index=B.max_index

    end_A_index=len(A.normalized_graph)-1
    end_B_index=len(B.normalized_graph)-1


    if(end_A_index>end_B_index):
        flag=1
    elif end_A_index<end_B_index:
        flag=2

    
    if max_A_index==0 and max_B_index==0:
        if flag==1:
            end_A_index=end_B_index
        elif flag==2:
            end_B_index=end_A_index

    elif max_A_index==end_A_index and max_B_index==end_B_index:
        if flag==1:
            start_A_index=end_A_index-end_B_index
        elif flag==2:
            start_B_index=end_B_index-end_A_index
    
    elif max_A_index!=0 and max_B_index!=0 and max_A_index!=end_A_index and max_B_index!=end_B_index:
        end_part_A=end_A_index-max_A_index
        end_part_B=end_B_index-max_B_index

        if end_part_A<=end_part_B:
            end_part=end_part_A
        else:
            end_part=end_part_B



        if max_A_index<=max_B_index:
            start_part=max_A_index
        else:
            start_part=max_B_index
        

        start_A_index=max_A_index-start_part
        start_B_index=max_B_index-start_part

        end_A_index=max_A_index+end_part
        end_B_index=max_B_index+end_part

        
    else:
        return(0,0)
    

    sum=0
    compare_A=A.normalized_graph[start_A_index:end_A_index]
    compare_B=B.normalized_graph[start_B_index:end_B_index]
    # print(len(compare_A),"vs",len(compare_B))
        
    for x in range(len(compare_A)):
        sum+=int(math.isclose(compare_A[x], compare_B[x],rel_tol=0.05))

       
    return (len(compare_A),sum)

def writing_to_xls_summary():

    file_name="summary.xlsx"

    p=Path.cwd()
    p=p/file_name
   
    with pd.ExcelWriter(p,engine="xlsxwriter") as writer:
        for x in range(len(r_list)):
            sheet_name=f"{x} summary"   
            data=r_list[x]
                    
            df=pd.DataFrame.from_dict(vars(data))
            df['duration_v']=df['duration_v'].astype(str)
            
            df.to_excel(writer,sheet_name=sheet_name,index=True, header=True,engine="xlsxwriter")

def writing_to_xls_analysis():

    file_name="analysis.xlsx"

    p=Path.cwd()
    p=p/file_name

    summary_list=[]
   
    with pd.ExcelWriter(p,engine="xlsxwriter") as writer:

        for item in ripple_connections:
            percent,position_from, position_to=item[-1]
            summary_list.append(f"from {position_from} to {position_to} there is a {round((percent)*100)}% match")
        
        df=pd.DataFrame(summary_list)
        df.to_excel(writer,sheet_name="pattern comparison summary",index=False, header=True,engine="xlsxwriter")

        for x,item in enumerate(ripple_connections):
            sheet_name=f"{x} matching"   
            data=item
            df2=pd.DataFrame(data,columns=["percentage match", "starting from", "compared with"])
            df2.to_excel(writer,sheet_name=sheet_name,index=True, header=True,engine="xlsxwriter")
    


def printing_batch_images():
    for x in range(len(r_list)):
        r_list[x].print_to_image(x)


def main():

    cvs_insert()  
    """
    basically inserts from the cvs , removes nulls and renames some column title
    """


    global trend_list, trend_list_count, threshold
    trend_list =[]

    trend_list=trend_setting()
    """
    sets the trends- basically takes the values extracted using pandas in cvs_insert and then compares with the one before and after.
     by storing the difference between those two we have negative and positive values
    """


    trend_list_count=[]
    threshold=1

    parting()
    """
    divides the values based on trend that changes sign- after we have the trend list we can easily break the whole data into sequences
    trend_list_count is initialezd there
    """


    ripple_doing()
    """
    creates a list of ripple class and loads all the data into each element
    """
    
    analize()
            
    writing_to_xls_summary()
    writing_to_xls_analysis()


    # printing_batch_images()




if __name__=="__main__":
    main()