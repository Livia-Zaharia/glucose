"""
Data division method- it takes the raw values from the Dataframe and splits it into sequences
"""

import copy
import typing as t
from datetime import datetime

import pandas as pd

from ripple import Ripple
from data_statistic import Ripple_stats


class Divide:
    """
    Class that contains methods for division
    """

    def __init__(self, glucose: pd.DataFrame = None, insulin: pd.DataFrame = None):
        self.glucose = glucose if glucose is not None else pd.DataFrame()
        self.insulin = insulin if insulin is not None else pd.DataFrame()

    def trend_setting(self) -> t.List[int]:
        """
        Method that sets the trends- basically takes the values extracted using pandas in csv_insert()
        and then compares with the one before and after.
        By storing the difference between those two, we have negative and positive values, which is the trend.
        """

        # Initialize an empty list to store the trends
        temp_trend_list = []

        # Iterate through each glucose value from the beginning to the second to last value
        for k in range(0, len(self.glucose) - 1):
            # Get the current glucose value (a_n) and convert it to an integer
            a_n = int(self.glucose.iloc[k, 1].astype(int))
            # Get the next glucose value (a_n_1) and convert it to an integer
            a_n_1 = int(self.glucose.iloc[k + 1, 1].astype(int))

            # Check if the current glucose value is equal to the next glucose value
            if a_n == a_n_1:
                # If they are equal, append 0 to the temp_trend_list
                temp_trend_list.append(0.0)
            else:
                # If they are not equal, append the difference between the next and current glucose value
                temp_trend_list.append(a_n_1 - a_n)

        # Append 0 to the temp_trend_list for the last glucose value
        temp_trend_list.append(0.0)

        # Return the list of trends
        return temp_trend_list

    def parting(self, trend_list: t.List[int], threshold: int) -> t.List[int]:

        """
        Method that divides the values based on trend that changes sign- 
        after we have the trend list we can easily break the whole data into sequences.
        It has an input of trend list- a list of trends (deltas between the current value and the next, 
        with sign to know if it increasease ore decreases) and a threshold, a limit of variation to consider as a change. Basically 
        the minimum value increment for a change min values to consider a change.
        
        """
        #the list that is going to be an output- list of items that represent the number of elements in a ripple
        trend_list_count = []

        #keeps track of the number that is going to be inserted in the list
        count = 0
        #how many positive or negatives values were counted till a certain point
        count_positive = 0
        count_negative = 0
        k = 0

        #keeps track of change in sign-if it increments up to two
        #it means we had two sign changes so if all the other conditions were satisfied we can append
        switch = 0

        #values of average of the trend- it will be compared with 
        # threshold so that you can round(or not) the values- like take into account only differences more than 5 units 
        positive_trend = 0
        negative_trend = 0

        #previous values of trends
        positive_trend_prev = 0
        negative_trend_prev = 0

        while k < len(self.glucose):

            #starts with the first trend in the list
            a_n = trend_list[k]

            #checks if it enters the branch with positive
            if a_n >= 0 and k < len(self.glucose):

                #while trends are positive continue to count how many they are(count_positive)
                #how many passes or general index (k)
                #and do a mass addition of the trend(positive_trend)

                while a_n >= 0 and k < len(self.glucose) - 1:
                    count_positive += 1
                    k += 1

                    positive_trend += a_n
                    a_n = trend_list[k]
                    count += 1

                #at the end we do the trend average (rewritten positive trend)
                #and we record we passed through a phase (the positive)
                positive_trend = positive_trend / count_positive
                switch += 1

            #checks if it will enter the branch with negative
            elif a_n < 0 and k < len(self.glucose):

                #while trends are negative continue to count how many they are(count_negative)
                #how many passes or general index-incremented since before (k)
                #and do a mass addition of the trend(negative_trend)

                while a_n < 0 and k < len(self.glucose) - 1:
                    count_negative += 1
                    k += 1

                    negative_trend += a_n
                    a_n = trend_list[k]
                    count += 1

                #at the end we do the trend average (rewritten negative trend)
                #and we record we passed through a phase (the negative)
                negative_trend = negative_trend / count_negative
                negative_trend = negative_trend * (-1)
                switch += 1
            
            #check if we had two changes of signs and at least 50 items
            #then we can partition, else do all of the above again until
            #  you fulfill these first criterias
            if switch >= 2 and count > 50:

                #values are reintialized to be used in the next loop
                count_positive = 0
                count_negative = 0

                #checks the second criterion, that the curves are not too flat
                #because since threshold is 1, not to pass this condition means that the variation was so low
                # (under 1), that it can be considered a flat liner. It checks positive trend and negative 
                # trend for the case where switch is 2 and the rest is for the cases where extra switches are needed to meet the first criteria
                
                if (positive_trend >= threshold and
                    negative_trend >= threshold) or (positive_trend_prev >= threshold and
                                                     negative_trend >= threshold) or (positive_trend >= threshold and
                                                                                      negative_trend_prev >= threshold):
                    trend_list_count.append(count)
                    count = 0
                    switch = 0

                positive_trend_prev = positive_trend
                negative_trend_prev = negative_trend

                positive_trend = 0
                negative_trend = 0

            if k == len(self.glucose) - 1:
                k += 1

        return trend_list_count

    def generate_ripples(self, trend_list: t.List[int], trend_list_count: t.List[int]) -> t.List[Ripple]:
        """
        Method that creates a list of Ripple instances and loads all the data into each element.
        Uses the method add_values() from class Ripple.
        """
        
        #here it is necessary to have that temp list because
        # we are going incrementing by the elements we extract from trend list count
        # so we have pairs of j,x (0,54)(54,56)(110,49) where trend list count was [54,56,49] that are going to slice as follows
        #[0:54][54:110][110:160] and it works because the slicing doesn't take the last value inclusevly
        
        temp_list=[]
        sum=0
        for elem in trend_list_count:
            temp_list.append((sum, elem))
            sum+=elem


        ripple_list = [
            self._create_ripple(j, x, trend_list)
            for (j,x) in temp_list
        ]

        return ripple_list

    def _create_ripple(self, j: int, x: int, trend_list: t.List[int]) -> Ripple:
        r_temp = Ripple()

        # Extract relevant data slices
        bg = self.glucose.iloc[j:j + x, 1]
        time = self.glucose.iloc[j:j + x, 0]
        trend = trend_list[j:j + x]

        # Add values to the Ripple instance
        r_temp.add_values(bg_value=bg, time_value=time, trend_value=trend)

        return r_temp

    @staticmethod
    def divide_by_iterable(data: Ripple) -> t.Tuple[dict, dict]:
        """
        Method that splits any given ripple into dictionaries of iterable and
        non-iterable elements.
        """

        # Create a deep copy of the original data dictionary to preserve input data.
        data_dict = copy.deepcopy(dict(vars(data)))

        # Initialize dictionaries to store iterable and non-iterable items.
        data_iter = {}
        data_noniter = {}

        # Iterate through the keys of the data dictionary.
        for item in data_dict.keys():
            try:
                # Check if the item is iterable.
                iter(data_dict[item])
            except TypeError:
                # If not iterable, add the item to the non-iterable dictionary.
                data_noniter[item] = data_dict[item]
            else:
                # If iterable, add the item to the iterable dictionary.
                data_iter[item] = data_dict[item]

        return data_iter, data_noniter

    def _split_insulin_by_ripple(self, ripple_list: t.List[Ripple]) -> t.List[t.List[t.Tuple[datetime, str, float]]]:
        """
        Method that splits the insulin dataframe stored into a list of n lists (the length of the ripple list received) with tuples
        structured as (timestamp, type of insulin, dosage).
        """
        insulin_storage = []
        i = 0

        # Iterate through the elements in the ripple_list.
        for elem in ripple_list:
            insulin_list = []

            # Loop until the insulin timestamp is less than or equal to the ripple end time or reaches the end of the
            # dataframe.
            while i < len(self.insulin) and self.insulin.iloc[i, 0] <= elem.end_t:
                # Append the insulin data as a tuple to the insulin_list.
                insulin_list.append(tuple(self.insulin.iloc[i, 0:3]))

                # Increment the index to process the next insulin record.
                i += 1

            # Add the insulin_list to insulin_storage.
            insulin_storage.append(insulin_list)

        return insulin_storage
    
    @staticmethod
    def _divide_by_fast_or_slow_insulin(single_ripple_insulin:t.List[t.Tuple[datetime, str, float]] ) -> t.Tuple[t.List, t.List]:
            """
            Method that splits any given single ripple insulin list
            into separate list for Fast-Acting and Long-Acting insulin

            """

            # Initialize lists to store fast acting and slow acting items.
            slow_insulin_seq=[]
            fast_insulin_seq=[]

            # Iterate through the list
            for item in single_ripple_insulin:
                if item[1] == "Fast-Acting":
                    fast_insulin_seq.append(item)
                else:
                    slow_insulin_seq.append(item)

            return  slow_insulin_seq, fast_insulin_seq
    
    def generate_ripple_statistics(self, ripple_list: t.List[Ripple], ripple_connections: t.List[t.List[t.Tuple[float, int, int]]]) -> t.List[Ripple_stats]:
        """
        Method that generates the ripple statistic list- a list where, for each ripple element
        you have the statistics related to it in relation to other ripples and itself
        """

        insulin_list=self._split_insulin_by_ripple(ripple_list)

        ripple_stats_list=[
            self._create_ripple_stats(i,ripple_list, ripple_connections,insulin_list)
            for i in range(len(ripple_list)) 
        ]

        return ripple_stats_list

    def _create_ripple_stats(self, index: int, ripple_list: t.List[Ripple], 
                             ripple_connections: t.List[t.List[t.Tuple[float, int, int]]], 
                             insulin_list:t.List[t.List[t.Tuple[datetime, str, float]]]) -> Ripple_stats:
        
        r_stat_temp= Ripple_stats(ripple_list[index])

        slow_insulin_seq, fast_insulin_seq=self._divide_by_fast_or_slow_insulin(insulin_list[index])
    
        r_stat_temp.add_values(index, slow_insulin_seq, fast_insulin_seq,ripple_connections)

        return r_stat_temp
        