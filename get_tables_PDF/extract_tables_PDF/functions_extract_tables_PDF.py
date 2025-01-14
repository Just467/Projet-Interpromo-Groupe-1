import camelot
import pandas as pd
import numpy as np
import pdfplumber
import regex as re


extract_tables_PDF_methods = ['lines', 'lines_strict', 'explicit']


def get_lines_stream(tables:camelot.core.TableList, axis:int)->list:
        """Get the coordinates of lines (of an axis) used by camelot to extract a table with Stream

        Args:
            tables (camelot.core.TableList): a camelot table
            axis (int): the axis of the target lines (0 for row, 1 for column)

        Returns:
            list: list of lines
        """
        lines = []
        for index, table in enumerate(tables):
            lines.append(table._bbox[1-axis])
            table_cells = table.cells
            if axis == 1:
                for cell in table_cells[0][1:]:
                    lines.append(cell.x1)
            else:
                for cell in table_cells[1:]:
                    lines.append(cell[0].y1)
            lines.append(table._bbox[3-axis])
        return lines


def extract_tables_page(page:pdfplumber.page.Page, page_number:int,pdf_path:str,
                        settings:dict, methods:list,
                        show_debugging:bool=False)->list:
    """Extract tables from a page of a PDF using a Page object from pdfplumber

    Args:
        pdf_path (str): path of the PDF file
        page (pdfplumber.page.Page): the pdfplumber page object
        page_number (int): the number of the page (starting from 0)
        settings (dict): settings of the function extract_tables from pdfplumber
        methods (list): methods to use parse the rows and the columns of the tables.
            The first value is for the rows, the second value for the columns.
            Both values must be one of lines, lines_strict, explicit.
        show_debugging (bool, optional): Whether to show the pdfplumber visual debugging or not.
            Defaults to False.

    Raises:
        ValueError: Both values of methods must be one of lines, lines_strict, explicit.

    Returns:
        list: a list of pandas dataframes, one for each table found.
    """
    if methods[0] not in extract_tables_PDF_methods or methods[1] not in extract_tables_PDF_methods:
        raise ValueError(f"Both values of methods must be one of {", ".join([str(elem) for elem in extract_tables_PDF_methods])}")
    
    df_tables = {}

    text_axes = np.where(np.array(methods) == 'explicit')[0]
    lines = {0:[], 1:[]}
    if any(text_axes):
        tables = camelot.read_pdf(pdf_path, flavor="stream", pages=f"{page_number+1}")
        for text_axis in text_axes:
            lines[text_axis] = get_lines_stream(tables, text_axis)
    
    if len(lines) > 1:
        settings["horizontal_strategy"], settings["vertical_strategy"] = methods[0], methods[1]
        settings["explicit_horizontal_lines"], settings["explicit_vertical_lines"] = lines[0], lines[1]
        all_tables = page.extract_tables(settings)
        tables_coordinates = page.find_tables(settings)
        tops = [table_coordinates.cells[0][1] for table_coordinates in tables_coordinates]
        if show_debugging:
            page.to_image().debug_tablefinder(settings).show()

    return all_tables, tops


def extract_titles_page(page: pdfplumber.page.Page,
                        pattern: str,
                        x_tolerance: float = 7.25, regex_match_pred=False) -> list:
    titles = []
    text = page.extract_text_lines()
    first_line = text[0]
    regex_match = re.search(pattern, first_line['text'])
    if regex_match:
        current_title = first_line['text']#.replace(regex_match.group(0), '')
        top_pred, regex_match_pred = first_line['top'], True

    for line in text[1:]:
        regex_match = re.search(pattern, line['text'])
        if regex_match: # on regarde si il y a un match
            if regex_match_pred: # si il y avait un match à la ligne précédente, on l'enregistre comme un titre
                titles.append((current_title, top_pred))
                regex_match_pred = False
            current_title = line['text']#.replace(regex_match.group(0), '')
            top_pred, regex_match_pred = line['top'], True
        elif regex_match_pred: # si il y avait un match à la ligne précédente et que cette ligne n'est pas un titre
            if  line['top']-top_pred <= x_tolerance: # si dans la tolérance, on rajoute cette ligne au titre
                current_title += " "+line['text']
                top_pred = line['top']
            else: # sinon on enregistre la ligne précédente comme étant un titre
                titles.append((current_title, top_pred))
                regex_match_pred = False
                
    if regex_match_pred:
        titles.append((current_title, top_pred))
    return titles


def get_all_raw_tables_PDF(PDF_file_settings:dict,
                           dict_tables:dict={}, pages=[-1], x_tolerance:float=7.25)->dict:
    """Function that uses complete_extract_tables_PDF to extract all the tables of multiple PDF files.

    Args:
        PDF_file_settings (dict): the settings to use for each PDF file.
        dict_tables (dict, optional): the dict returned by the fuction. Contains all the tables. Defaults to {}.
        pages (list, optional): list of pages to explore. Defaults to [-1], exploring all pages.

    Returns:
        dict: returns dict_tables with all the new tables extracted.
        Tables are organized by PDF_file and by title based on the titles found in the PDF.
    """
    for PDF_file_name, settings in PDF_file_settings.items():
        path, extract_settings, methods = settings['path'], settings['extract_settings'], settings['methods']
        pattern = settings['pattern']
        last_title=('',0)
        dict_tables_pdf = {}
        with pdfplumber.open(path) as pdf:
            for page_number, page in enumerate(pdf.pages):
                if page_number in pages or pages==[-1]:
                    # extracting titles and tables from one page
                    tables, tops = extract_tables_page(page, page_number,path,
                                                       extract_settings, methods)
                    titles = [last_title] + extract_titles_page(page,pattern)
                    # associating titles and tables
                    start_index = 1
                    current_title_name = titles[0][0]
                    for table, top in zip(tables, tops):
                        for index_title, title in enumerate(titles[start_index:], start=start_index):
                            if title[1] - top >= x_tolerance:
                                break
                            current_title_name = title[0]
                        try:
                            dict_tables_pdf[current_title_name] = dict_tables_pdf[current_title_name] + [pd.DataFrame(table)]
                        except KeyError:
                            dict_tables_pdf[current_title_name] = [pd.DataFrame(table)]
                        start_index = index_title
                    
        dict_tables[PDF_file_name] = dict_tables_pdf
    return dict_tables
