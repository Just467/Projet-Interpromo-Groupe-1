import pandas as pd
import pdfplumber
import sys
sys.path.append('get_tables_PDF')
from extract_tables_PDF_page import extract_tables_page, extract_titles_page, extract_rows, is_header_row
from process_table import clean_df, unpivot_df

def get_all_raw_tables_PDF(PDF_file_settings:dict,
                           final_tables:list=[], pages=[-1], x_tolerance:float=7.25,
                           split=True)->dict:
    """Function that uses complete_extract_tables_PDF to extract all the tables of multiple PDF files.

    Args:
        PDF_file_settings (dict): the settings to use for each PDF file.
        dict_tables (dict, optional): the dict returned by the fuction. Contains all the tables. Defaults to {}.
        pages (list, optional): list of pages to explore. Defaults to [-1], exploring all pages.

    Returns:
        dict: returns dict_tables with all the new tables extracted.
        Tables are organized by PDF_file and by title based on the titles found in the PDF.
    """
    path, extract_settings, methods = PDF_file_settings['path'], PDF_file_settings['extract_settings'], PDF_file_settings['methods']
    pattern = PDF_file_settings['pattern']
    last_title, last_title_page = ('',0), 0
    with pdfplumber.open(path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            if page_number in pages or pages==[-1]:
                # extracting tables from one page
                titles = extract_titles_page(page,pattern)
                if titles:
                    titles = [last_title] + titles
                    last_title, last_title_page = titles[-1], page_number
                else:
                    titles = [last_title]
                # extracting tables from one page and rows to have all the correct and cleaned tables
                extracted_tables = extract_tables_page(page, page_number,path,
                                                       extract_settings, methods,
                                                       show_debugging=True)
                extracted_table_rows = extract_rows(page, page_number,path,
                                                    extract_settings)
                header_list = [[is_header_row(row)for row in extracted_table_row] for extracted_table_row in extracted_table_rows]
                cleaned_tables = []
                for table, sub_header_list in zip(extracted_tables, header_list):
                    cleaned_tables = cleaned_tables + clean_df(pd.DataFrame(table), sub_header_list)
                # associating titles and tables
                start_index = 1
                current_title_name = titles[0][0]
                for df, top, df_header_list in cleaned_tables:
                    for index_title, title in enumerate(titles[start_index:], start=start_index):
                        if title[1] - top >= x_tolerance:
                            break
                        start_index = index_title
                        current_title_name = title[0]
                    final_tables.append({'table': df,
                                         'title': current_title_name,
                                         'pages':list(range(last_title_page, page_number+1)),
                                         'header_list': df_header_list})
    if split:
        for index, final_table in enumerate(final_tables):
            print(final_table['table'])
            print(final_table['header_list'])
            final_tables[index]['table'] = unpivot_df(final_table['table'], final_table['header_list'])
    return final_tables