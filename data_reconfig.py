"""
Data reconfiguration method to format any different type of data structure into structures accepted by DataManager

"""
from __future__ import annotations

import typing as t


class Modify:
    """
    Class of methods for restructuring data

    """

    def get_name_and_type(self, data_iter: t.Dict[str, t.List]) -> t.Dict[str, str]:
        """
        Method that receives a Dict with iterable values of EQUAL length, that contain immutable values, which in turn are not iterable,
        and returns a Dict containing the same keys with the type of the elements that construct the iterable 
        
        """
        simplified_data_iter = {}

        for elem in list(data_iter.keys()):
            simplified_data_iter.setdefault(elem, list(data_iter[elem])[0])

        return simplified_data_iter

    def get_name_and_value(self, data_iter: t.Dict[str, t.List], i: int) -> t.Dict[str, int | float | str]:
        """
        Method that receives a Dict with iterable values of EQUAL length,  that contain immutable values, which in turn are not iterable,
        and returns a Dict containing the same keys with the value at a given position 
        
        """

        simplified_data_iter_row = {}

        for elem in list(data_iter.keys()):
            simplified_data_iter_row.setdefault(elem, list(data_iter[elem])[i])

        return simplified_data_iter_row
