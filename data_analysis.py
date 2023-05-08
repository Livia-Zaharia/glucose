"""
Module for graphical analysis of the ripple
"""
import math
import typing as t

from ripple import Ripple


class Analyze:
    """
    Class that contains methods for analysis
    """

    def __init__(self, ripple_list: t.List[Ripple]):
        self.ripple_list = ripple_list

    def _compare_ripple_items(self, ripple1: Ripple, ripple2: Ripple) -> t.Tuple[float, float]:
        """
        Compare two Ripple items and return their percentages of close values.

        Args:
            ripple1/ripple2: Ripple objects
        
        Returns:
            tuple:
            percent_ripple1,percent_ripple2: float representing the percent value of the number of values 
                                            extracted in comparison and the total length of the graph
        """
        common_interval, close_value_count = self._compare_two_graphs(ripple1, ripple2)

        if close_value_count != 0:
            percent_ripple1 = round(close_value_count / len(ripple1.normalized_graph), 2)
            percent_ripple2 = round(close_value_count / len(ripple2.normalized_graph), 2)
            return percent_ripple1, percent_ripple2
        return 0, 0

    def _create_list_ripple_pairs(self, index1: int, ripple1: Ripple, index2: int, ripple2: Ripple,
                              connections: t.List[t.List[t.Tuple[float, int, int]]]) -> None:
        """
        Compare a pair of Ripple items and update the connections list accordingly.

        Args:
            index1/index2:int, position of ripple in the ripple list
            ripple1/ripple2: ripple objects
            connections: a list of lists with tuples that gets updated by using the same address.
                it starts off as an empty list and then it grows into the list that is modified at each run
        """
        percent_ripple1, percent_ripple2 = self._compare_ripple_items(ripple1, ripple2)

        if percent_ripple1 != 0 and percent_ripple2 != 0:
            connections[index1].append((percent_ripple1, index1, index2))
            connections[index2].append((percent_ripple2, index2, index1))

    def compare_graphs(self) -> t.List[t.List[t.Tuple[float, int, int]]]:
        """
        Method that compares two graphs by taking each graph and comparing it to all the other graphs in the
        ripple_list. It returns a list [with as many lists as there are elements in ripple_list[each of which contain
        a list of tuples(percentage, origin and comparison) that have not null values]]

        Returns:
            connections: the list of lists of tuples(float, int, int)
        """
        # Initialize connections list with empty lists.
        connections = [[] for _ in self.ripple_list]

        # Generate all unique pairs of indices in ripple_list.
        pairs = [(i, j) for i in range(len(self.ripple_list)) for j in range(i + 1, len(self.ripple_list))]

        # Iterate through each unique pair of indices and compare the corresponding Ripple items.
        for index1, index2 in pairs:
            self._create_list_ripple_pairs(index1, self.ripple_list[index1], index2, self.ripple_list[index2], connections)

        # Sort each list of tuples in connections.
        for item in connections:
            item.sort()

        return connections

    @staticmethod
    def _compare_two_graphs(ripple_a: Ripple, ripple_b: Ripple) -> t.Tuple[int, int]:
        """
        Method that returns comparison of two graphs going by value. It determines the common interval between the
        graphs starting from the max in normalized form. Then it returns a tuple having (total length compared,
        number of items in that comparison that are relatively close in value to each other)

        Args:
            ripple_a/ripple_b: Ripple objects to be compared
        
        Returns:
            a tuple composed of:
            len(compare_a): number of elements that were compared out of the length of the ripple
            sum_of_elements: sum of true values- basically how many elements out of those in 
                            len(compare_a) were a close enough match
        """

        #start indexes of ripple A and ripple B- index- as in list[index]
        #we are going to use list positioning to go through the values
        start_a_index = 0
        start_b_index = 0
        
        flag = 0

        #max value index for ripple A and B
        max_a_index = ripple_a.max_index
        max_b_index = ripple_b.max_index
        
        #end index for ripple A and B
        end_a_index = len(ripple_a.normalized_graph) - 1
        end_b_index = len(ripple_b.normalized_graph) - 1
        
        #select which ripple is longer in absolute values
        #if ripple A is longer then flag=1
        #if ripple B is longer then flag=2
        if end_a_index > end_b_index:
            flag = 1
        elif end_a_index < end_b_index:
            flag = 2
        
        #case 1- when maximum value is placed at the begining of the graph
        #in this case we must choose which ripple is longer using (flag)
        #and to trim the graph according to who is longer
        #trimming= setting the values of start and end of the ripples in such way that both
        #ripple slices have the same length according to the indexes they came in with
        if max_a_index == 0 and max_b_index == 0:
            
            #since ripple A is longer then the end of ripple A will take the
            #same index as that of ripple B or the opposite in the else
            if flag == 1:
                end_a_index = end_b_index
            elif flag == 2:
                end_b_index = end_a_index

        #case 2 -when maximum value is placed at the end of the graph
        #in this case the index is not directly edited        
        elif max_a_index == end_a_index and max_b_index == end_b_index:
            
            #since ripple A is longer it is going to start from the difference between the two
            #similar for ripple B longer
            if flag == 1:
                start_a_index = end_a_index - end_b_index
            elif flag == 2:
                start_b_index = end_b_index - end_a_index

        #case 3- when maximum value is somwhere in the center for both ripple A and ripple B        
        elif max_a_index != 0 and max_b_index != 0 and max_a_index != end_a_index and max_b_index != end_b_index:
            
            #end part is the diference between the maximum value and the end for both ripples.
            # At the end we need a common end part value to be added to the max value index
            end_part_a = end_a_index - max_a_index
            end_part_b = end_b_index - max_b_index
            
            #choosing the smaller end part because it will always be included in the longer one
            if end_part_a <= end_part_b:
                end_part = end_part_a
            else:
                end_part = end_part_b
            
            if max_a_index <= max_b_index:
                start_part = max_a_index
            else:
                start_part = max_b_index
            
            #define the index of the split. considering we have a fixed value- max,
            # everything we do will be in regards to it. so the interval will be defined
            # as starting from max-the smallest start part and 
            # ending in max +the smallest ending part
            start_a_index = max_a_index - start_part
            start_b_index = max_b_index - start_part
            end_a_index = max_a_index + end_part
            end_b_index = max_b_index + end_part
        
        #case 4- any other case means that the ripple are not comparable, for example having a ripple which starts with the max
        #and another that ends with the max- they can have no common overlapping since the pivot value, the max, is in extremes
        else:
            return 0, 0
        
        #value that counts how many elements are similar
        sum_of_elements = 0
        
        #the actual splicing
        compare_a = ripple_a.normalized_graph[start_a_index:end_a_index]
        compare_b = ripple_b.normalized_graph[start_b_index:end_b_index]
        
        #the comparison element by element
        for x in range(len(compare_a)):
            sum_of_elements += int(math.isclose(compare_a[x], compare_b[x], rel_tol=0.05))

        return len(compare_a), sum_of_elements
