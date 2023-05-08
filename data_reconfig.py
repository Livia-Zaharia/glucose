"""
Data reconfiguration method to format any different type of data structure into structures accepted by DataManager

"""
from __future__ import annotations

import typing as t


def get_name_and_type(data_dict: t.Dict[str, t.List]) -> t.Dict[str, str]:
    """
    Method that receives a Dict with iterable values of EQUAL length, that contain immutable values, which in turn
    are not iterable, and returns a Dict containing the same keys with the type of the elements that construct the
    iterable

    Args:
        data_dict: a dict that contains the key as string and the values as iterable values of only immutable values and Equal length
    
    Returns:
        dict that has the same keys and values of str type containing the type of elements in the values of the recieved dict
    """
    return {key: value[0] for key, value in data_dict.items()}


def get_name_and_value(data_iter: t.Dict[str, t.List], index: int) -> t.Dict[str, int | float | str]:
    """
    Method that receives a Dict with iterable values of EQUAL length, that contain immutable values, which in turn
    are not iterable, AND an index and returns a Dict containing the same keys with the value at the given position

    Args:
        data_iter:a dict that contains the key as string and the values as iterable values of only immutable values and EQUAL length 
        index: the position of the element in the iterable list we want to access

    Returns:
        dict having the same keys but as values a single element from the iterable index position
    """
    return {key: value[index] for key, value in data_iter.items()}


def convert_from_tuple_list_to_dict(input_list: t.List[t.Tuple], key_list: t.List[str]) -> t.Dict[str, t.List]:
    """
    Method to convert a list of x tuples of n elements into a dict with n keys with lists of x values
    """
    # Initialize an empty list for each key in the key_list and store it in the result_dict dictionary
    result_dict = {key: [] for key in key_list}

    # Iterate through each tuple (item) in the input_list
    for item in input_list:
        # Iterate through each category_value in the item tuple, along with its index (k)
        for k, category_value in enumerate(item):
            # Append the current category_value to the corresponding key's list in result_dict
            result_dict[key_list[k]].append(category_value)

    # Return the resulting dictionary
    return result_dict

def convert_list_of_tuples_to_string(sequence:t.List[tuple]) -> str:
    
    text_list=[]
    for elem in sequence:
        text_list.append(str(elem))
    
    final_text='\n'.join(text_list)
    return final_text
    
