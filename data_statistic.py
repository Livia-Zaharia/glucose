"""
Module to record connections/ripple
"""
import typing as t
from ripple import Ripple
from data_analysis import round_to_multiple as rm
import datetime

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
        #about the ripple
        self.base_max_t=base_ripple.max_t
        self.base_min_t=base_ripple.min_t
        self.is_ascending=True
        
        #about the graph
        self.max_graph_similarity=""
        
        #about the time
        self.duration_category=(rm(base_ripple.duration_v.total_seconds(),3600))/3600
        # self.duration_similarity=[]
        
        #about the long acting insulin
        self.slow_insulin_seq=[]
        self.slow_time_vs_max=0
        self.slow_time_vs_min=0
                
        #about the fast acting insulin
        self.fast_insulin_seq=[]
        self.fast_time_vs_max=0
        self.fast_time_vs_min=0
        
    def add_values(self, index:int, slow_insulin_seq, fast_insulin_seq,ripple_list:t.List[Ripple], ripple_connections:t.List[t.List[t.Tuple[float, int, int]]], time_list:t.List[float]):
        
        percent, position_from, position_to =ripple_connections[index][-1]
        self.max_graph_similarity=f"{percent*100}% -from {position_from}-to {position_to}"

        self.slow_insulin_seq=slow_insulin_seq
        if self.slow_insulin_seq:
            slow_insulin_exists=True
        else:
            slow_insulin_exists=False

        self.fast_insulin_seq=fast_insulin_seq
        if self.fast_insulin_seq:
            fast_insulin_exists=True
        else:
            fast_insulin_exists=False

        if self.base_max_t < self.base_min_t:
            self.is_ascending=False

        # self._check_duration_category(time_list)
        self._check_insulin_positioning(slow_insulin_exists,fast_insulin_exists)

    def _check_duration_category(self, time_list:t.List[float]) -> t.List[int]:
        """
        Method that recieves the self.duration_category type and the time_list and returns the list of indices where the ripples have the same length
        """
        for index, value in enumerate(time_list):
            if self.duration_category == value:
                self.duration_similarity.append(index)

    @staticmethod
    def time_in_range(start, end, x) ->bool:
        """Return true if x is in the range [start, end]"""
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

    def _check_insulin_positioning(self,slow_insulin_exists,fast_insulin_exists):
        if slow_insulin_exists:
            self.slow_time_vs_max,self.slow_time_vs_min = self.analize_positions(self.slow_insulin_seq)
        
        if fast_insulin_exists:
            self.fast_time_vs_max,self.fast_time_vs_min = self.analize_positions(self.fast_insulin_seq)            

    def analize_positions(self,interval_list:list) -> t.Tuple[datetime.timedelta,datetime.timedelta]:
        """
        Method used to check how an interval behaves- always compare with the base ripple. It works in between two intervals
        glucose interval- given by max glucose value and min glucose value, and insulin interval with start and end insulin value
        it returns the tuple from_max, to_min starting from the asumption that insulin shots are made when glucose is high and as 
        a direct result it will go down. since this is so there will be cases in which the tuple returned will be ("NEXT/PREV","NEXT/PREV")
        because that case is not feasible in the context of this ripple   

        """     
        max_glucose_time=self.base_max_t
        min_glucose_time=self.base_min_t

        #list that will be used to check the position of insulin events
        interval_list_check=[]
        sum=0

        for elem in interval_list:
            value=self.time_in_range(max_glucose_time,min_glucose_time,elem[0])
            interval_list_check.append(value)
            sum+=int(value)

        start_insulin_time=interval_list[0][0]
        end_insulin_time=interval_list[-1][0]

        if sum == len(interval_list_check):
            #it means the insulin events are grouped and can be considered as one, individual shot. 
            #this shot will be positioned in between the values of glucose interval (first case)
            
            from_max=(start_insulin_time-max_glucose_time) if (start_insulin_time>max_glucose_time) else (max_glucose_time-start_insulin_time)
            to_min=(end_insulin_time-min_glucose_time) if (end_insulin_time>min_glucose_time) else (min_glucose_time-end_insulin_time)
            return (from_max, to_min)
        
        elif sum == 0 :
            #it means the insulin events are grouped and can be considered as one, individual shot. 
            #this shot will be positioned outside the glucose interval (second case)
            
            if self.is_ascending:
                #when the glucose interval is ascending
                if(start_insulin_time >= max_glucose_time):

                    #the case in which the insulin interval is outside at the end of the glucose interval
                    # meaning that the glucose has risen and action was needed to take it down
                    # to_min is not of importance since it will affect the min in the next ripple, not this one

                    from_max=start_insulin_time-max_glucose_time
                    to_min="NEXT"
                    return (from_max, to_min)
                else:

                    #the case in which the insulin interval is outside at the begining of the glucose interval
                    #is_ascending is true and that means it referenced the previous ripple
                    return("PREV","PREV")
           
            else:
                #when the glucose interval is descending

                if(end_insulin_time <= max_glucose_time):
                    #the case where the insulin interval is positioned outside at the begining of the glucose interval
                    #is_ascending false shows that it starts of in high value

                    from_max=(start_insulin_time-max_glucose_time) if (start_insulin_time>max_glucose_time) else (max_glucose_time-start_insulin_time)
                    to_min=(end_insulin_time-min_glucose_time) if (end_insulin_time>min_glucose_time) else (min_glucose_time-end_insulin_time)
                   
                    return (from_max, to_min)
                else:
                    #the case in which the insulin interval is after the end of a decreasing interval
                    #as a usecase it can mean the folowing- had a low value, ate, and then because it started to rise 
                    #extra insulin was needed

                    return("NEXT","NEXT")


        else:
            #these are the casese that insulin interval contains one of the ends of the glucose interval

            if interval_list_check[0]:
                #it means it starts of in the glucose interval only to leave it after a while

                if self.is_ascending:
                    #it means it contains the max glucose value of this ripple
                    # and the min value will be found in the next ripple

                    from_max=end_insulin_time-max_glucose_time
                    to_min="NEXT"
                    return (from_max, to_min)
                else:
                    #it means it contains the min glucose value of this ripple
                    #basically it means you are having shots while in low, so the only normal case it could apply
                    # it would mean that a ceratin part of insulin was made before the low- and that will affect this ripple 
                    # while the rest is for the next. so we will use a shortenend version of the interval
                    short_interval=[]

                    for i,elem in enumerate (interval_list_check):
                        if elem:
                            short_interval.append(interval_list[i])
                    
                    
                    start_insulin_time=short_interval[0][0]
                    end_insulin_time=short_interval[-1][0]
                    
                    from_max=(start_insulin_time-max_glucose_time) if (start_insulin_time>max_glucose_time) else (max_glucose_time-start_insulin_time)
                    to_min=(end_insulin_time-min_glucose_time) if (end_insulin_time>min_glucose_time) else (min_glucose_time-end_insulin_time)
                    
                    return (from_max, to_min)
                    
            else:
                #it starts of outside the glucose interval and enters it later
                if not self.is_ascending:
                    #it means it contians the max glucose value
                    #it uses the last value of the interval because given as it was a composed shot 
                    #the complete duration of injection has to be after the last value because previous shots did not work

                    from_max=end_insulin_time-max_glucose_time
                    to_min=end_insulin_time-min_glucose_time
                    return (from_max, to_min)
                else:

                    #it means it contains the low glucose value
                    #since the glucose interval grows it means that not sufficent insulin was provided so any value that is found between
                    # the min and tha max will affect the current ripple
                    
                    short_interval=[]
                    
                    for i,elem in enumerate (interval_list_check):
                        if not elem:
                            short_interval.append(interval_list[i])
                                        
                    start_insulin_time=short_interval[0][0]
                    end_insulin_time=short_interval[-1][0]
                    
                    from_max=(end_insulin_time-max_glucose_time) if (end_insulin_time>max_glucose_time) else (max_glucose_time-end_insulin_time)
                    to_min="NEXT"
                    return (from_max, to_min)


        
        

