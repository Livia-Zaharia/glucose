"""
Module to record connections/ripple
"""
import typing as t
from ripple import Ripple
from data_analysis import round_to_multiple as rm

class Ripple_stats:
    """
    Object that stores statistic atributes of a ripple
    base= the original ripple- taken as to be able to call the base values
    max_graph_similarity= tuple containitng the value, the origin as index and the direction as index for the most similar ripple in regard to the graph
    duration_category= float value that gives the round number in hour in which that ripple falls into
    duration_similarity= a list of indexes of similar ripple in regards to the duration category
    slow_insulin_seq/fast_insulin= lists of tuple (datetime, str,float) where there are only values of slow/fast acting insulin
    slow/fast_ insulin_exists= bool flag to check or not tests for these parameters 
    """

    def __init__(self, base_ripple:Ripple):
        self.base=base_ripple
        self.max_graph_similarity=()
        self.duration_category=0
        self.duration_similarity=[]
        self.slow_insulin_seq=[]
        self.slow_insulin_exists=False
        self.fast_insulin_seq=[]
        self.fast_insulin_exists=False

    def add_values(self, index:int, slow_insulin_seq, fast_insulin_seq,ripple_list:t.List[Ripple], ripple_connections:t.List[t.List[t.Tuple[float, int, int]]], time_list:t.List[float]):
        self.max_graph_similarity=ripple_connections[index][-1]
        self.duration_category=rm(ripple_list[index].duration_v.total_seconds(),3600)

        self.slow_insulin_seq=slow_insulin_seq
        if len(self.slow_insulin_seq)!=0:
            self.slow_insulin_exists==True

        self.fast_insulin_seq=fast_insulin_seq
        if len(self.fast_insulin_seq)!=0:
            self.fast_insulin_exists==True

        self._check_duration_category(time_list)

    def _check_duration_category(self, time_list:t.List[float]) -> t.List[int]:
        """
        Method that recieves the self.duration_category type and the time_list and returns the list of indices where the ripples have the same length
        """
        for index, value in enumerate(time_list):
            if self.duration_category == value:
                self.duration_similarity.append(index)

        

