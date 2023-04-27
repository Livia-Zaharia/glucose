"""
Module for exporting and displaying data. It works on the display functions which are not covered 
by the Database Manager or used in conjencture with the methods of class Ripple.
It can be used as standalone provided the values asked
"""

import typing as t
from pathlib import Path

import pandas as pd

from constants import ANALYSIS_XLSX_FILE_NAME
from ripple import Ripple

CURRENT_PATH_CWD = Path.cwd()


def create_dataframe(summary_list: t.List) -> pd.DataFrame:
    """
    Create a DataFrame from a given list.

    Args:
        summary_list: A list containing data to be converted into a DataFrame.

    Returns:
        A Pandas DataFrame containing the data from the input list.
    """
    # Convert the input list to a DataFrame
    df = pd.DataFrame(summary_list)

    return df


def write_dataframe_to_xls_file(df: pd.DataFrame, file_path: Path, sheet_name: str) -> None:
    """
    Write the DataFrame to an Excel file with the given sheet name.

    Args:
        df: A Pandas DataFrame to be written to the Excel file.
        file_path: The output file path.
        sheet_name: The name of the sheet in the Excel file.
    """
    # Use the ExcelWriter context manager to write the DataFrame to an Excel file
    with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
        # Write the DataFrame to the Excel file with the specified sheet name, without index and with headers
        df.to_excel(writer, sheet_name=sheet_name, index=False, header=True, engine="xlsxwriter")


def write_analysis_to_xls_file(summary_list: t.List, sheet_name: str) -> None:
    """
    Write a list to an Excel file as a new sheet with the given sheet name.

    Args:
        summary_list: A list containing data to be written to the Excel file.
        sheet_name: The name of the sheet in the Excel file.
    """
    # Combine the current working directory path with the file name
    file_path = CURRENT_PATH_CWD / ANALYSIS_XLSX_FILE_NAME

    # Create a DataFrame from the input list
    df = create_dataframe(summary_list=summary_list)
    # Write the DataFrame to the Excel file
    write_dataframe_to_xls_file(df=df, file_path=file_path, sheet_name=sheet_name)


def create_data_directory(index: int, base_path: Path) -> Path:
    """
    Create a data directory for a given index within the base path.

    Args:
        index: The index of the ripple used for naming the directory.
        base_path: The base path where the data directory should be created.

    Returns:
        The created data directory Path object.
    """
    # Create a new directory path for the ripple with the given index
    data_path = base_path / f"Ripple_no{index}"
    # Create the new directory and its parents if they don't exist
    data_path.mkdir(parents=True, exist_ok=True)

    return data_path


def batch_write_graphs_to_disk(ripple_list: t.List[Ripple], base_path: Path,
                               should_write_as_html: bool = False) -> None:
    """
    Batch write ripple graphs to disk in either png or html format.

    Args:
        ripple_list: A list of Ripple objects containing the graph data.
        base_path: The base path where the data directories should be created.
        should_write_as_html: If True, write the graphs in HTML format; otherwise, write them in PNG format.
    """
    # Iterate through the list of ripples
    for index, ripple in enumerate(ripple_list):
        # Create a new data directory for the ripple
        data_path = create_data_directory(index=index, base_path=base_path)
        # Write the ripple graph to the data directory
        ripple.create_graphic(index=index, should_write_html=should_write_as_html, data_path=data_path)
