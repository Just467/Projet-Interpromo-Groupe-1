import pandas as pd
import sys
sys.path.append('get_tables_PDF')
from extract_tables_PDF.string_operations import find_all_largest_common_substrings, delete_first_occurrence

concat_df_methods = ['row', 'column']

def concat_df(df:pd.core.frame.DataFrame, method:str):
    """Concat dataframe cells into a single string following an axis (either row or column)

    Args:
        df (pd.core.frame.DataFrame): a dataframe
        method (str): the method to concat the dataframe

    Raises:
        ValueError: method must be one of row, column

    Returns:
        the concat string
    """
    if method not in concat_df_methods:
        raise ValueError(f"Value must be one of {", ".join([str(elem) for elem in concat_df_methods])}")
    if method=='row':
        concat_rows = []
        for index, row in df.iterrows():
            concat_rows.append(row.astype(str).str.cat(sep=''))
        return concat_rows
    if method=='column':
        concat_col = []
        for column_name in df:
            concat_col.append(df[column_name].astype(str).str.cat(sep=''))
        return concat_col

def merge_stream_pdfplumber(pdfplumber_df, stream_df):
    str_cat_rows, str_cat_columns = concat_df(pdfplumber_df, 'row'), concat_df(stream_df, 'column')
    merged_table = []
    for index_row, row in enumerate(str_cat_rows):
        print(index_row)
        merged_row = []
        for index_col, column in enumerate(str_cat_columns):
            common_strings = find_all_largest_common_substrings(row, column)
            if common_strings:
                row = delete_first_occurrence(row, common_strings[0])
                merged_row.append(common_strings[0])
            else:
                merged_row.append(None)
        merged_table.append(merged_row)
        print(merged_table)
        print()
    return pd.DataFrame(merged_table)

