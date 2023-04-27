"""
Data division method- it takes the raw values from the Dataframe and splits it into sequences
"""

import copy
import typing as t
from datetime import datetime

import pandas as pd

from ripple import Ripple


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

        """

        trend_list_count = []

        count = 0
        count_positive = 0
        count_negative = 0
        k = 0

        switch = 0

        positive_trend = 0
        negative_trend = 0

        positive_trend_prev = 0
        negative_trend_prev = 0

        while k < len(self.glucose):

            a_n = trend_list[k]

            if a_n >= 0 and k < len(self.glucose):

                while a_n >= 0 and k < len(self.glucose) - 1:
                    count_positive += 1
                    k += 1

                    positive_trend += a_n
                    a_n = trend_list[k]
                    count += 1

                positive_trend = positive_trend / count_positive
                switch += 1

            elif a_n < 0 and k < len(self.glucose):

                while a_n < 0 and k < len(self.glucose) - 1:
                    count_negative += 1
                    k += 1

                    negative_trend += a_n
                    a_n = trend_list[k]
                    count += 1

                negative_trend = negative_trend / count_negative
                negative_trend = negative_trend * (-1)
                switch += 1

            if switch >= 2 and count > 50:

                count_positive = 0
                count_negative = 0

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
        ripple_list = [
            self.create_ripple(j, x, trend_list)
            for j, x in enumerate(trend_list_count)
        ]

        return ripple_list

    def create_ripple(self, j: int, x: int, trend_list: t.List[int]) -> Ripple:
        r_temp = Ripple()

        # Extract relevant data slices
        bg = self.glucose.iloc[j:j + x, 1]
        time = self.glucose.iloc[j:j + x, 0]
        trend = trend_list[j:j + x]

        # Add values to the Ripple instance
        r_temp.add_values(bg_value=bg, time_value=time, trend_value=trend)

        return r_temp

    def divide_by_iterable(self, data: Ripple) -> t.Tuple[dict, dict]:
        """
        Method that splits any given ripple into dictionaries of iterable and respectively non iterable elements
        """

        to_be_processed = copy.deepcopy(dict(vars(data)))
        data_iter = copy.deepcopy(to_be_processed)
        data_noniter = copy.deepcopy(to_be_processed)

        for item in list(to_be_processed.keys()):

            try:
                iter(to_be_processed[item])
            except TypeError:
                data_iter.pop(item)
            else:
                data_noniter.pop(item)

        return (data_iter, data_noniter)

    def split_insulin_by_ripple(self, ripple_list: t.List[Ripple]) -> t.List[t.List[t.Tuple[datetime, str, float]]]:
        """
        Method that splits the insulin dataframe stored into a list of n lists (the lenght of the ripple list recieved) with tuples
        structured as(timestamp-type of insulin-dosage)
        """
        insulin_storage = []
        i = 0
        for elem in ripple_list:
            insulin_list = []
            while self.insulin.iloc[i, 0] <= elem.end_t:
                insulin_list.append((self.insulin.iloc[i, 0], self.insulin.iloc[i, 1], self.insulin.iloc[i, 2]))
                i += 1
            insulin_storage.append(insulin_list)
        return insulin_storage
