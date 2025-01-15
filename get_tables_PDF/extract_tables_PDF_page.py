import camelot
import pandas as pd
import numpy as np
import pdfplumber
import regex as re

extract_tables_PDF_methods = ['lines', 'lines_strict', 'explicit']

def is_header_row(row, page_height:int=842,
                  numeric_pattern:str=r'^[\d.,\s€$£¥]*(?: *ans)?$', year_pattern:str=r'^20[0-2]\d$'):
    """_summary_

    Args:
        row (_type_): _description_
        numeric_pattern (str, optional): _description_. 
        year_pattern (str, optional): _description_. 

    Returns:
        _type_: _description_
    """
    top = 0
    for cell in row:
        if cell is not None:
            if cell.text is not None:
                top = cell.y1
                cell_text = cell.text.strip()
                if cell_text != '' and re.match(numeric_pattern, cell_text) and not re.match(year_pattern, cell_text):
                    return False, page_height-top
    if top != 0:
        return ('header', page_height-top)
    else:
        return('none', page_height-top)

def extract_rows(page:pdfplumber.page.Page, page_number:int,pdf_path:str,
                 settings={}):
    """
    Renvoie une liste de 'rows' à mettre dans is_header

    Args:
        pdf_path (str): pdf path
        page (pdfplumber.page.Page): pdfplumber page object
        page_number (int)
        user_settings (dict): settings rentrés par l'utilisateur

    Returns:
        list: liste des rows
    """

    def get_row_corners(row):
        """
        Renvoie les coordonnées des 2 coins d'une row

        Args:
            row (list): List des coordonnées de chaque cell [(x0, top, x1, bottom), ...].

        Returns:
            list: coordonnées des 2 coins [x1, y1, x2, y2].

        Raises:
            ValueError: Si vide ou contient des `None`
        """
        filtered_row = [cell for cell in row if cell is not None]
        if not filtered_row:
            raise ValueError("Row is empty or contains only None values.")

        x1, top, _, _ = filtered_row[0]
        _, _, x2, bottom = filtered_row[-1]

        return [x1, top, x2, bottom]

    # à adapter selon user_setting
    tables_rows = []
    tables = page.find_tables(settings)
    for table in tables:
        rows = []
        for _, row in enumerate(table.rows):
            added_none = False  # Variable de contrôle pour éviter les doublons
            try:
                x1, y1, x2, y2 = get_row_corners(row.cells)
                str_row_corners = f"{x1},{page.height - y1},{x2},{page.height - y2}"
                camelot_row = camelot.read_pdf(
                    pdf_path,
                    flavor="stream",
                    pages=f"{page_number + 1}",
                    table_areas=[str_row_corners],
                    row_tol=1000
                )
                rows.append(camelot_row[0].cells[0])

            except ValueError as e:
                if not added_none:
                    rows.append([None])
                    added_none = True
                print(f"Skipping row due to error: {e}")

            except Exception as e:
                if not added_none:
                    rows.append([None])
                    added_none = True
                print(f"Unexpected error: {e}")
        tables_rows.append(rows)
    return tables_rows


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
        page (pdfplumber.page.Page): the pdfplumber page object
        page_number (int): the number of the page (starting from 0)
        pdf_path (str): path of the original PDF file
        settings (dict): settings of the function extract_tables from pdfplumber
        methods (list): methods to use parse the rows and the columns of the tables.
            The first value is for the rows, the second value for the columns.
            Both values must be one of : lines, lines_strict, explicit.
            Explicit use Camelot with Stream method to determine the lines that will be passed to pdfplumber.
        show_debugging (bool, optional): Whether to show the pdfplumber visual debugging or not.
            Defaults to False.

    Raises:
        ValueError: Both values of methods must be one of : lines, lines_strict, explicit.

    Returns:
        list: a list of tuple, one for each table.
        Each tuple contains (in this order):
            - the raw table extracted with pdfplumber
            - the y-coordinates in the PDF of the top line of the table
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
        if show_debugging:
            page.to_image().debug_tablefinder(settings).show()

    return all_tables


def extract_titles_page(page: pdfplumber.page.Page,
                        pattern: str,
                        x_tolerance: float = 7.25) -> list:
    """Extract all titles from a page of a PDF using a Page object from pdfplumber.
       Title are detected with a regex.

    Args:
        page (pdfplumber.page.Page): the pdfplumber page object.
        pattern (str): a string defining the regex to use to detect titles.
        x_tolerance (float, optional): Tables within that range are still considered to be under the current title, even though they are above it.
        Defaults to 7.25.

    Returns:
        list: _description_
    """
    titles, regex_match_pred = [], False
    text = page.extract_text_lines()
    first_line = text[0]
    regex_match = re.search(pattern, first_line['text'])
    if regex_match:
        current_title = first_line['text']#.replace(regex_match.group(0), '')
        top_pred, regex_match_pred = first_line['top'], True

    for line in text[1:]:
        regex_match = re.search(pattern, line['text'])
        if regex_match: # if the current line is a title
            if regex_match_pred: # if the previous line was a title, we save the previous line as a title
                titles.append((current_title, top_pred))
                regex_match_pred = False
            current_title = line['text']#.replace(regex_match.group(0), '')
            top_pred, regex_match_pred = line['top'], True
        elif regex_match_pred: # if the current line is not a title but the previous line was
            if  line['top']-top_pred <= x_tolerance: # if within tolerance, this line is considered to be part of the title
                current_title += " "+line['text']
                top_pred = line['top']
            else: # if not, the previous line is saved as a title
                titles.append((current_title, top_pred))
                regex_match_pred = False
                
    if regex_match_pred:
        titles.append((current_title, top_pred))
    return titles
