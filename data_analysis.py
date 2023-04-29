import math
import typing as t
from ripple import Ripple

def round_to_multiple(number: float, multiple: float) -> float:
        """
        Simple method of rounding up to a set value
        
        """
        return multiple * round(number / multiple)

class Analyze:
    """
    Class that contains methods for analysis
    """

    def __init__(self, ripple_list: t.List[Ripple]):
        self.ripple_list = ripple_list

    def _compare_ripple_items(self, ripple1: Ripple, ripple2: Ripple) -> t.Tuple[float, float]:
        """
        Compare two Ripple items and return their percentages of close values.
        """
        common_interval, close_value_count = self._compare_two_graphs(ripple1, ripple2)

        if close_value_count != 0:
            percent_ripple1 = round(close_value_count / len(ripple1.normalized_graph), 2)
            percent_ripple2 = round(close_value_count / len(ripple2.normalized_graph), 2)
            return percent_ripple1, percent_ripple2
        return 0, 0

    def _compare_ripple_pairs(self, index1: int, ripple1: Ripple, index2: int, ripple2: Ripple,
                              connections: t.List[t.List[t.Tuple[float, int, int]]]) -> None:
        """
        Compare a pair of Ripple items and update the connections list accordingly.
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
        """
        # Initialize connections list with empty lists.
        connections = [[] for _ in self.ripple_list]

        # Generate all unique pairs of indices in ripple_list.
        pairs = [(i, j) for i in range(len(self.ripple_list)) for j in range(i + 1, len(self.ripple_list))]

        # Iterate through each unique pair of indices and compare the corresponding Ripple items.
        for index1, index2 in pairs:
            self._compare_ripple_pairs(index1, self.ripple_list[index1], index2, self.ripple_list[index2], connections)

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
        """
        start_a_index = 0
        start_b_index = 0
        flag = 0
        max_a_index = ripple_a.max_index
        max_b_index = ripple_b.max_index
        end_a_index = len(ripple_a.normalized_graph) - 1
        end_b_index = len(ripple_b.normalized_graph) - 1
        if end_a_index > end_b_index:
            flag = 1
        elif end_a_index < end_b_index:
            flag = 2
        if max_a_index == 0 and max_b_index == 0:
            if flag == 1:
                end_a_index = end_b_index
            elif flag == 2:
                end_b_index = end_a_index
        elif max_a_index == end_a_index and max_b_index == end_b_index:
            if flag == 1:
                start_a_index = end_a_index - end_b_index
            elif flag == 2:
                start_b_index = end_b_index - end_a_index
        elif max_a_index != 0 and max_b_index != 0 and max_a_index != end_a_index and max_b_index != end_b_index:
            end_part_a = end_a_index - max_a_index
            end_part_b = end_b_index - max_b_index
            if end_part_a <= end_part_b:
                end_part = end_part_a
            else:
                end_part = end_part_b
            if max_a_index <= max_b_index:
                start_part = max_a_index
            else:
                start_part = max_b_index
            start_a_index = max_a_index - start_part
            start_b_index = max_b_index - start_part
            end_a_index = max_a_index + end_part
            end_b_index = max_b_index + end_part
        else:
            return 0, 0
        sum_of_elements = 0
        compare_a = ripple_a.normalized_graph[start_a_index:end_a_index]
        compare_b = ripple_b.normalized_graph[start_b_index:end_b_index]
        for x in range(len(compare_a)):
            sum_of_elements += int(math.isclose(compare_a[x], compare_b[x], rel_tol=0.05))

        return len(compare_a), sum_of_elements

    def compare_duration(self) -> t.List[float]:
        """
        Method for comparing duration.It returns a list with all duration in hours
        """
        time_list = []
        for item in self.ripple_list:
            time = item.duration_v.total_seconds()
            time = round_to_multiple(time, 3600)
            time_list.append(time / 3600)
        # time_list.sort()
        # time_list = set(time_list)
        # time_list = list(time_list)
        return time_list