"""
Module to record connections for each ripple
"""
import typing as t
from ripple import Ripple
import datetime


def round_to_multiple(number: float, multiple: float) -> float:
        """
        Simple method of rounding up to a set value
        Args:
        
        """
        return multiple * round(number / multiple)

def time_in_range(start:datetime.time, end:datetime.time, x:datetime.time) ->bool:
        """
        Return true if x is in the range [start, end]
        """
        
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end



class Ripple_stats:
    """
    Object that stores statistic attributes of a ripple, that is why it is instanced with a ripple object

    Args:
        base_max_t/base.min_t: the original ripple max/min value time- taken from the original ripple at the given index
        is_ascending: boolean value showing if the graph is ascending or not (which comes first- the min or the max in the glucose interval)

        max_graph_similarity: string converted from tuple using the construction f"{round((percent) * 100)}% -from {position_from}-to {position_to}"
                            showing the best similarity of the graph

        duration_category: float value that gives the round number in hour in which that ripple falls into
    
        slow_insulin_seq/fast_insulin: lists of tuple (datetime, str,float) where there are only values of slow/fast acting insulin
        slow/fast_ insulin_exists: bool flag to check or not tests for these parameters 
        slow/fast_time vs max: timedelta values of the interval between the closest insulin time and the max value 
        slow/fast_time vs min: time delta values of the interval between the closest insulin time and the min value
     
    """

    def __init__(self, base_ripple:Ripple):
        #about the ripple
        self.base_max_t=base_ripple.max_t
        self.base_min_t=base_ripple.min_t
        self.is_ascending=True
        
        #about the graph
        self.max_graph_similarity=""
        
        #about the time
        self.duration_category=(round_to_multiple(base_ripple.duration_v.total_seconds(),3600))/3600
                
        #about the long acting insulin
        self.slow_insulin_seq=[]
        self.slow_time_vs_max=datetime.timedelta(0)
        self.slow_time_vs_min=datetime.timedelta(0)
                
        #about the fast acting insulin
        self.fast_insulin_seq=[]
        self.fast_time_vs_max=datetime.timedelta(0)
        self.fast_time_vs_min=datetime.timedelta(0)
        
    def add_values(self, index:int, slow_insulin_seq:t.List[t.Tuple[datetime.time, str,float]],
                   fast_insulin_seq:t.List[t.Tuple[datetime.time, str,float]], 
                   ripple_connections:t.List[t.List[t.Tuple[float, int, int]]]) -> None:
        """
        Method of adding all the values into the Ripple_Stats object
        """
        percent, position_from, position_to =ripple_connections[index][-1]
        self.max_graph_similarity=f"{round((percent) * 100)}% -from {position_from}-to {position_to}"

        self.slow_insulin_seq=slow_insulin_seq
        if slow_insulin_seq:
            slow_insulin_exists=True
        else:
            slow_insulin_exists=False

        self.fast_insulin_seq=fast_insulin_seq
        if fast_insulin_seq:
            fast_insulin_exists=True
        else:
            fast_insulin_exists=False

        if self.base_max_t < self.base_min_t:
            self.is_ascending=False

       
        self._check_insulin_positioning(slow_insulin_exists,fast_insulin_exists)

   
    def _check_insulin_positioning(self,slow_insulin_exists:bool,fast_insulin_exists:bool) ->None:
        """
        Method that starts the checking for insulin position in relation to glucose values  
        """
        if slow_insulin_exists:
            self.slow_time_vs_max,self.slow_time_vs_min = self.analyze_positions(self.slow_insulin_seq)
        
        if fast_insulin_exists:
            self.fast_time_vs_max,self.fast_time_vs_min = self.analyze_positions(self.fast_insulin_seq)            

    def analyze_positions(self,interval_list:t.List[t.Tuple[datetime.time, str,float]]) -> t.Tuple[datetime.timedelta,datetime.timedelta]:
        """
        Method used to check how an interval behaves- always compare with the base ripple. It works in between two intervals
        glucose interval- given by max glucose value and min glucose value, 
        and insulin interval with start and end insulin value
        it returns the tuple from_max, to_min starting from the assumption that insulin shots are made when glucose is high and as 
        a direct result it will go down. since this is so there will be cases in which the tuple returned will be ("NEXT/PREV","NEXT/PREV")
        because that case is not feasible in the context of this ripple, meaning that the effects of the shot are influencing the other ripples, not the current one   
        """     
        #start of the glucose interval- note that this is not the start and end value of the interval 
        # according to time, but the max and min values- no matter the order of occurrence

        max_glucose_time=self.base_max_t
        min_glucose_time=self.base_min_t

        #list that will be used to check the position of insulin events
        interval_list_check=[]
        sum=0
        switch=-1
        prev_value=2

        #checks whether all elements in the insulin list are inside or outside or both 
        # inside/outside of the range- and marks the position
        for elem in interval_list:
            value=time_in_range(max_glucose_time,min_glucose_time,elem[0])
            interval_list_check.append(value)
            sum+=int(value)
            if prev_value != int(value):
                switch+=1
            prev_value=int(value)

        #marks the start and end of the insulin interval- to be noted here we do take into account 
        # start and end chronologicaly because all event are ordered when extracted from the csv
        #also as a logical implementation we take into account only the end values on the presumption that no matter 
        # how many shots were taken in between it did not provide the neccesary amount of insulin to lower/influence the glucose
        start_insulin_time=interval_list[0][0]
        end_insulin_time=interval_list[-1][0]

        if sum == len(interval_list_check):
            #Case 1
            #----------------min/max----------start_insulin-------------end_insulin----------------min/max---------------------
            # it means the insulin events are grouped and can be considered as one, individual shot. 
            #this shot will be positioned in between the values of glucose interval
            
            from_max=(start_insulin_time-max_glucose_time) if (start_insulin_time>max_glucose_time) else (max_glucose_time-start_insulin_time)
            to_min=(end_insulin_time-min_glucose_time) if (end_insulin_time>min_glucose_time) else (min_glucose_time-end_insulin_time)
            return (from_max, to_min)
        
        elif sum == 0 :
            #case 2
            #it means the insulin events are grouped and can be considered as one, individual shot. 
            #this shot will be positioned outside the glucose interval
            
            if self.is_ascending:
                #when the glucose interval is ascending- here is where is checked whether max or min is first

                if(start_insulin_time >= max_glucose_time):

                    #case 2.1.1
                    #----------------min---------------------max------------start_insulin-------------------end_insulin-----
                    # the case in which the insulin interval is outside at the end of the glucose interval
                    # meaning that the glucose has risen and action was needed to take it down
                    # to_min is not of importance since it will affect the min in the next ripple, not this one

                    from_max=(start_insulin_time-max_glucose_time) if (start_insulin_time>max_glucose_time) else (max_glucose_time-start_insulin_time)
                    return (from_max, "NEXT")
                else:

                    #case 2.2.1
                    #----start_insulin-------end_insulin----------------min----------------------max---------------------
                    # the case in which the insulin interval is outside at the beginning of the glucose interval
                    #is_ascending is true and that means it referenced the previous ripple
                    to_min=(end_insulin_time-min_glucose_time) if (end_insulin_time>min_glucose_time) else (min_glucose_time-end_insulin_time)
                    return("PREV",to_min)
           
            else:
                #when the glucose interval is descending

                if(end_insulin_time <= max_glucose_time):
                    #case 2.2.2
                    #---start_insulin------end_insulin--------------------max------------------min---------------------
                    # the case where the insulin interval is positioned outside at the beginning of the glucose interval
                    #is_ascending false shows that it starts of in high value

                    from_max=(start_insulin_time-max_glucose_time) if (start_insulin_time>max_glucose_time) else (max_glucose_time-start_insulin_time)
                    to_min=(end_insulin_time-min_glucose_time) if (end_insulin_time>min_glucose_time) else (min_glucose_time-end_insulin_time)
                   
                    return (from_max, to_min)
                else:
                    #case 2.1.2
                    #----------------max--------------min------------------------start_insulin---------end_insulin-------
                    # the case in which the insulin interval is after the end of a decreasing interval
                    #as a usecase it can mean the folowing- had a low value, ate, and then because it started to rise 
                    #extra insulin was needed

                    return("NEXT","NEXT")


        else:
            #these are the cases that insulin interval contains one of the ends of the glucose interval or contains the glucose interval itself

            if interval_list_check[0]:
                #case 3
                # it means it starts of in the glucose interval only to leave it after a while.
                #it will always contain the end

                if self.is_ascending:
                    #case 3.2
                    #----------------min----------start_insulin--------------max----------end_insulin-----------
                    # it means it contains the max glucose value of this ripple
                    # and the min value will be found in the next ripple

                    from_max=(start_insulin_time-max_glucose_time) if (start_insulin_time>max_glucose_time) else (max_glucose_time-start_insulin_time)
                    to_min="NEXT"
                    return (from_max, to_min)
                else:
                    #case 3.1
                    #----------------max----------start_insulin-----------end_insulin---------min------------XXend_insulin---------
                    # it means it contains the min glucose value of this ripple
                    #basically it means you are having shots while in low, so the only normal case it could apply
                    # it would mean that a certain part of insulin was made before the low- and that will affect this ripple 
                    # while the rest is for the next. so we will use a shortened version of the interval
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
                #case4
                # it starts off outside the glucose interval and enters it later
                #or it can start outside- go in - and after go out
                #it will always contain the start of the glucose interval
                if switch == 2:
                    #case4.3
                    #------start_insulin----------min/max----------------------min/max------------end_insulin---------
                    # it contains the whole glucose interval
                    return("PREV","NEXT")
                
                if not self.is_ascending:
                    #case 4.2
                    #-----start_insulin-----------max------------------end_insulin----------------min---------------------
                    # it means it contains the max glucose value
                    #it was a composed shot because previous shots did not work

                    from_max=(start_insulin_time-max_glucose_time) if (start_insulin_time>max_glucose_time) else (max_glucose_time-start_insulin_time)
                    to_min=(end_insulin_time-min_glucose_time) if (end_insulin_time>min_glucose_time) else (min_glucose_time-end_insulin_time)
                    return (from_max, to_min)
                else:

                    #case 4.1
                    #------XXstart_insulin----------min----------start_insulin-------------end_insulin----------------max---------------------
                    #it means it contains the low glucose value
                    #since the glucose interval grows it means that not sufficient insulin was provided so any value that is found between
                    # the min and tha max will affect the current ripple
                    
                    short_interval=[]
                    
                    for i,elem in enumerate (interval_list_check):
                        if elem:
                            short_interval.append(interval_list[i])
                                        
                    start_insulin_time=short_interval[0][0]
                    end_insulin_time=short_interval[-1][0]
                    
                    from_max=(start_insulin_time-max_glucose_time) if (start_insulin_time>max_glucose_time) else (max_glucose_time-start_insulin_time)
                    to_min="NEXT"
                    return (from_max, to_min)


        
        

