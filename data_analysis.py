"""
Module for analysis
"""

import math
import typing as t

from ripple import Ripple


class Analyze:
    """
    Class that contains methods for analysis
    """
    def __init__(self,r_list:t.List[Ripple]):
        self.r_list=r_list

    def _compare_two_graphs(self,A:Ripple, B:Ripple)->t.Tuple[int,int]:
        """
        Method that returns comparison of two graphs going by value.
        It determines the common interval between the graphs starting from the max in normalized form.
        Then it returns a tuple having (total length compared, number of items in that comparison that are relatively close in value to each other)
        """

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

        for x in range(len(compare_A)):
            sum+=int(math.isclose(compare_A[x], compare_B[x],rel_tol=0.05))


        return (len(compare_A),sum)

    def compare_graphs(self)->t.List[t.List[t.Tuple[float,int,int]]]:
        """
        Method that compares two graphs by taking each graph and comparing it to all the other graphs in the r-List.
        It returns a list [with as many list as there are elements in 
        ripple_list[each of witch contain a list of tuples(percentage, origin and comparison) that have not null values]]
        """
        ripple_connections=[]

        for item in self.r_list:
            ripple_connections.append([])


        for search_item in self.r_list:
            for compare_item in self.r_list[self.r_list.index(search_item)+1:]:

                percent_search_value=0
                percent_compare_value=0

                common_interval,isclose_values=self._compare_two_graphs(search_item, compare_item)

                if isclose_values!=0:
                    percent_search_value=round(isclose_values/len(search_item.normalized_graph),2)
                    percent_compare_value=round(isclose_values/len(compare_item.normalized_graph),2)
                    ripple_connections[self.r_list.index(search_item)].append((percent_search_value,self.r_list.index(search_item),self.r_list.index(compare_item)))
                    ripple_connections[self.r_list.index(compare_item)].append((percent_compare_value,self.r_list.index(compare_item),self.r_list.index(search_item)))


        for item in ripple_connections:
            item.sort()

        return ripple_connections

    def round_to_multiple(self, number:float,multiple:float)->float:
        """
        Simple method of rounding up to a set value
        
        """
        return multiple*round(number/multiple)

    def compare_duration(self)->t.List[int]:
        """
        Method for comparing duration.It returns a list with all unique duration in hours
        """
        time_list=[]
        for item in self.r_list:
            time=item.duration_v.total_seconds()
            time=self.round_to_multiple(time,3600)
            time_list.append(time/3600)

        time_list.sort()
        time_list=set(time_list)
        time_list=list(time_list)

        return time_list


