from __future__ import annotations

import math

from ripple import Ripple


class Analyze:
    def __init__(self, r_list):
        self.r_list = r_list

    def _compare_two_graphs(self, A: Ripple, B: Ripple) -> tuple:

        start_a_index = 0
        start_b_index = 0

        flag = 0

        max_a_index = A.max_index
        max_b_index = B.max_index

        end_a_index = len(A.normalized_graph) - 1
        end_b_index = len(B.normalized_graph) - 1

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

        sum = 0
        compare_a = A.normalized_graph[start_a_index:end_a_index]
        compare_b = B.normalized_graph[start_b_index:end_b_index]

        for x in range(len(compare_a)):
            sum += int(math.isclose(compare_a[x], compare_b[x], rel_tol=0.05))

        return len(compare_a), sum

    def compare_graphs(self) -> list | tuple:
        ripple_connections = []

        for item in self.r_list:
            ripple_connections.append([])

        for search_item in self.r_list:
            for compare_item in self.r_list[self.r_list.index(search_item) + 1:]:

                percent_search_value = 0
                percent_compare_value = 0

                common_interval, isclose_values = self._compare_two_graphs(search_item, compare_item)

                if isclose_values != 0:
                    percent_search_value = round(isclose_values / len(search_item.normalized_graph), 2)
                    percent_compare_value = round(isclose_values / len(compare_item.normalized_graph), 2)
                    ripple_connections[self.r_list.index(search_item)].append(
                        (percent_search_value, self.r_list.index(search_item), self.r_list.index(compare_item)))
                    ripple_connections[self.r_list.index(compare_item)].append(
                        (percent_compare_value, self.r_list.index(compare_item), self.r_list.index(search_item)))

        for item in ripple_connections:
            item.sort()

        return ripple_connections

    def round_to_multiple(self, number: float, multiple: float) -> float:
        """
        Simple function of rounding up to a set value
        
        """
        return multiple * round(number / multiple)

    def compare_duration(self) -> list:
        time_list = []
        for item in self.r_list:
            time = item.duration_v.total_seconds()
            time = self.round_to_multiple(time, 3600)
            time_list.append(time / 3600)

        time_list.sort()
        time_list = set(time_list)
        time_list = list(time_list)

        return time_list
