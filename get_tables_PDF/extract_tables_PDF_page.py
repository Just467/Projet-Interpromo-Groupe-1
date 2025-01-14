import camelot
import pandas as pd
import numpy as np
import pdfplumber
import regex as re


extract_tables_PDF_methods = ['lines', 'lines_strict', 'explicit']

def is_header_row(tables, min_year=2020, max_year=2025):
    """
    Vérifie si une ligne Camelot est un header.

    Args:
        tables (list): Liste de tables Camelot.
        min_year (int): Année minimale autorisée.
        max_year (int): Année maximale autorisée.

    Returns:
        bool: True si une ligne est un header, False sinon.
    """
    # Regex pour détecter les chiffres, devises, points, virgules et espaces
    numeric_pattern = r'^[\d.,\s€$£¥]*$'

    def is_pure_number(value):
        """Vérifie si une valeur est un entier positif."""
        return re.match(r"^\d+$", str(value).strip()) is not None

    def is_valid_year(value):
        """Vérifie si une valeur est une année valide."""
        return min_year <= int(value) <= max_year

    for table in tables:
        for row in table.cells:
            numerical_values = []
            for cell in row:
                if cell is None or cell.text is None:
                    continue

                cell_text = cell.text.strip()

                # Vérifie si la cellule contient une valeur numérique
                if re.fullmatch(numeric_pattern, cell_text):
                    if is_pure_number(cell_text):
                        numerical_values.append(int(cell_text))

            # Vérification des conditions
            if numerical_values:
                if len(numerical_values) == 1:
                    # Une seule valeur numérique : Vérifier si c'est une année en première cellule
                    if is_valid_year(numerical_values[0]) and row[0].text.strip() == str(numerical_values[0]):
                        return True
                    else:
                        return False
                elif all(is_valid_year(num) for num in numerical_values):
                    # Toutes les valeurs numériques sont des années
                    return True
                else:
                    # Des valeurs numériques non conformes
                    return False

    # Si aucune valeur numérique n'est trouvée, c'est un header
    return True

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
        tables_coordinates = page.find_tables(settings)
        tops = [table_coordinates.cells[0][1] for table_coordinates in tables_coordinates]
        if show_debugging:
            page.to_image().debug_tablefinder(settings).show()

    return [(all_table, top) for all_table, top in  zip(all_tables, tops)]


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
