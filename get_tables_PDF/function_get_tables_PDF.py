import pandas as pd
import pdfplumber
import sys
sys.path.append('get_tables_PDF')
from extract_tables_PDF_page import extract_tables_page, extract_titles_page
from process_table import clean_df, unpivot_df

def get_all_raw_tables_PDF(PDF_file_settings:dict,
                           final_tables:list=[], pages=[-1], x_tolerance:float=7.25)->dict:
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
                # extracting titles and tables from one page
                extracted_tables = extract_tables_page(page, page_number,path,
                                                       extract_settings, methods)
                titles = extract_titles_page(page,pattern)
                if titles:
                    titles = [last_title] + titles
                    last_title_page = page_number
                else:
                    titles = [last_title]
                # associating titles and tables
                start_index = 1
                current_title_name = titles[0][0]
                for table, top in extracted_tables:
                    for index_title, title in enumerate(titles[start_index:], start=start_index):
                        if title[1] - top >= x_tolerance:
                            break
                        current_title_name = title[0]
                    final_tables.append({'table': pd.DataFrame(table), 'title': current_title_name, 'pages':list(range(last_title_page, page_number+1))})
                else:
                    index_title = -1
                start_index = index_title       
    return final_tables