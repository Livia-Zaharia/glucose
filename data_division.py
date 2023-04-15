"""
Data division method- it takes the raw values from the Dataframe and splits it into sequences
"""

import copy
import typing as t

import pandas as pd

from ripple import Ripple


class Divide:
    """
    Class that contains methods for division
    """

    def __init__(self,glucose:pd.DataFrame=[]):
        self.glucose=glucose

    def trend_setting(self)->t.List[int]:
        """
        Method that sets the trends- basically takes the values extracted using pandas in csv_insert()
        and then compares with the one before and after.
        By storing the difference between those two we have negative and positive values which is the trend.
        
        """

        temp_trend_list= []

        for k in range(0,len(self.glucose)-1):
            a_n=int(self.glucose.iloc[k,1].astype(int))
            a_n_1=int(self.glucose.iloc[k+1,1].astype(int))
            
            
            if a_n==a_n_1:
                temp_trend_list.append(0.0)
            else:
                temp_trend_list.append(a_n_1-a_n)
            
        temp_trend_list.append(0.0)
        return temp_trend_list

    def parting(self,trend_list:t.List[int],threshold:int)->t.List[int]:

        """
        Method that divides the values based on trend that changes sign- 
        after we have the trend list we can easily break the whole data into sequences.

        """

        trend_list_count=[]

        count=0
        count_positive=0
        count_negative=0
        k=0

        switch=0

        positive_trend=0
        negative_trend=0

        positive_trend_prev=0
        negative_trend_prev=0

        
        while k<len(self.glucose):
        
            a_n=trend_list[k]
        
            if a_n>=0 and k<len(self.glucose):
                
                while a_n>=0 and k<len(self.glucose)-1:
                    count_positive+=1
                    k+=1
                    
                    positive_trend+=a_n
                    a_n=trend_list[k]
                    count+=1
                
                
                positive_trend=positive_trend/count_positive
                switch+=1

            elif a_n<0 and k<len(self.glucose):
                
                while a_n<0 and k<len(self.glucose)-1:
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

                if (positive_trend>=threshold and
                     negative_trend>=threshold) or (positive_trend_prev>=threshold and
                     negative_trend>=threshold) or (positive_trend>=threshold and
                     negative_trend_prev>=threshold):
                    
                    trend_list_count.append(count)
                    count=0
                    switch=0
                
                positive_trend_prev=positive_trend
                negative_trend_prev=negative_trend

                positive_trend=0
                negative_trend=0
            
                
            if k==len(self.glucose) - 1:
                    k+=1
        
        return trend_list_count

    def generate_ripples(self, trend_list: t.List[int], trend_list_count: t.List[int]) -> t.List[Ripple]:
        """
        Method that creates a list of ripple class and loads all the data into each element.
        Uses the method add_values() from class Ripple.
        
        """
        ripple_list = []
        j = 0

        for x in trend_list_count:
            r_temp = Ripple()

            bg: pd.DataFrame = self.glucose.iloc[j:j + x, 1]
            time: pd.DataFrame = self.glucose.iloc[j:j + x, 0]
            trend = trend_list[j:j + x]

            r_temp.add_values(bg_value=bg, time_value=time, trend_value=trend)

            ripple_list.append(r_temp)

            j += x

        return ripple_list

    def divide_by_iterable(self,data:Ripple)->t.Tuple[dict,dict]:
        """
        Method that splits any given ripple into dictionaries of iterable and respectively non iterable elements
        """

        to_be_processed=copy.deepcopy(dict(vars(data)))
        data_iter=copy.deepcopy(to_be_processed)
        data_noniter=copy.deepcopy(to_be_processed)

        for item in list(to_be_processed.keys()):
                    
            try:
                iter(to_be_processed[item])
            except TypeError:
                data_iter.pop(item)
            else:
                data_noniter.pop(item)

        return (data_iter,data_noniter)