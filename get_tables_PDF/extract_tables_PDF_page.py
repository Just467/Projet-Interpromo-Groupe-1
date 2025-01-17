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

###############################

def extract_areas(rows, index_headers):
    """
    Extract table areas by grouping rows until encountering a header or NaN.

    Args:
        rows (list): List of (x1, y1, x2, y2) coordinates for each row.
        index_headers (list): Indices of rows that are headers.

    Returns:
        list: List of table areas as (x1, y1, x2, y2).
    """
    areas = []  # To store table areas
    i = 0

    while i < len(rows):
        current_area = rows[i][:]  # Copy the current row's coordinates

        if i + 1 < len(rows) and (i + 1 in index_headers):
            # If the next row is a header, this area stands alone
            area_type = "alone"
        else:
            # Group rows until encountering a header or the end
            while (
                i + 1 < len(rows)
                and i + 1 not in index_headers
            ):
                i += 1
                current_area[2:] = rows[i][2:]  # Extend the area to include the next row

            area_type = "group"

        area_desc = {"area_coords": current_area, "area_type": area_type}
        areas.append(area_desc)
        i += 1

    return areas


def get_vertical_lines_from_camelot(table_areas, page, page_number, pdf_path):
    """
    Extract vertical lines as objects from Camelot tables.

    Args:
        tables (camelot.core.TableList): List of tables detected by Camelot.
        top_coord (float): Top coordinate of the row.
        bottom_coord (float): Bottom coordinate of the row.

    Returns:
        list: Vertical lines formatted as pdfplumber-compatible objects.
    """
    areas_with_vertical_lines = []
    for area in table_areas:
        try:
            x1, top, x2, bottom = area["area_coords"]
            str_area_corners = f"{x1},{page.height - top},{x2},{page.height - bottom}"
            row_camelot = camelot.read_pdf(
                        pdf_path,
                        flavor="stream",
                        pages=f"{page_number + 1}",
                        table_areas=[str_area_corners],
                        row_tol = 1000,
            )

            vertical_lines = []
            for row in row_camelot[0].cells:
                nb_cells = len(row)
                for cell_index in range(nb_cells):
                    cell = row[cell_index]

                    # Right edge of the current cell
                    vertical_lines.append({
                        "x0": cell.x1,
                        "x1": cell.x1,
                        "top": top,
                        "bottom": bottom,
                        "height": bottom - top,
                        "orientation": "v",
                        "object_type": "line"
                    })

                    # Add the right edge of the last cell
                    if cell_index == nb_cells - 1:
                        vertical_lines.append({
                            "x0": cell.x2,
                            "x1": cell.x2,
                            "top": top,
                            "bottom": bottom,
                            "height": bottom - top,
                            "orientation": "v",
                            "object_type": "line"
                    })
        
            area["vertical_lines"] = vertical_lines
            areas_with_vertical_lines.append(area)
        except ValueError as e:
            print(f"Skipping area due to ValueError: {e}")
            continue
        except Exception as e:
            print(f"Unexpected error: {e}")
            continue
    return areas_with_vertical_lines

def get_row_coords(row):
    """
    Convert a row's bounding box from PdfPlumber into the format required by Camelot's `table_areas`.

    Args:
        row (list): List of cell coordinates [(x0, top, x1, bottom), ...].

    Returns:
        list: Bounding box [x1, y1, x2, y2].

    Raises:
        ValueError: If the row is empty or contains only `None` values.
    """
    filtered_row = [cell for cell in row if cell is not None]
    if not filtered_row:
        raise ValueError("Row is empty or contains only None values.")

    x1, top, _, _ = filtered_row[0]
    _, _, x2, bottom = filtered_row[-1]

    return [x1, top, x2, bottom]

def get_table_area(area_list, page_height):
    """
    Convert area coordinates to Camelot's `table_areas` format.

    Args:
        area_list (list): List of coordinates [x1, y1, x2, y2].
        page_height (float): Height of the PDF page.

    Returns:
        str: Bounding box in Camelot format "x1,y1,x2,y2".
    """
    x1, y1, x2, y2 = area_list
    return f"{x1},{page_height - y1},{x2},{page_height - y2}"


def get_index_headers_and_row_areas(table, page, page_number, pdf_path):    
    def get_row_corners(row):
        filtered_row = [cell for cell in row if cell is not None]
        if not filtered_row:
            raise ValueError("Row is empty or contains only None values.")
        x1, top, _, _ = filtered_row[0]
        _, _, x2, bottom = filtered_row[-1]

        return [x1, top, x2, bottom]
    
    index_headers = []
    row_areas = []
    for index, row in enumerate(table.rows):
        try:
            x1, top, x2, bottom = get_row_corners(row.cells)
            str_row_corners = f"{x1},{page.height - top},{x2},{page.height - bottom}"
            row_areas.append([x1, top, x2, bottom])
            camelot_row = camelot.read_pdf(
                pdf_path,
                flavor="stream",
                pages=f"{page_number + 1}",
                table_areas=[str_row_corners],
                row_tol=1000
            )

            if is_header_row(camelot_row[0].cells[0])[0]=='header':
                index_headers.append(index)
        except ValueError as e:
            print(f"Skipping row due to error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    return index_headers, row_areas

def snap_vertical_lines(row_desc):
    """
    Ajuste les coordonnées des verticales_lines des rows de type "alone".

    Args:
        row_desc (list): Liste des dictionnaires représentant les rows avec leurs verticales_lines.

    Returns:
        list: Liste des verticales_lines modifiées.
    """
    all_lines = []  # Liste pour concaténer toutes les verticales_lines

    for i, row in enumerate(row_desc):
        if row["area_type"] != "alone":
            all_lines.extend(row["vertical_lines"])
            continue

        vertical_lines = row["vertical_lines"]

        # Trouver le next_row de type "group"
        next_row = None
        for k in range(i + 1, len(row_desc)):
            if row_desc[k]["area_type"] == "group":
                next_row = row_desc[k]
                break

        # Si aucun next_row de type "group" n'est trouvé, ne rien faire
        if not next_row:
            all_lines.extend(vertical_lines)
            continue

        next_vertical_lines = next_row["vertical_lines"]

        for j, line in enumerate(vertical_lines):
            x0, x1 = line["x0"], line["x1"]

            if j == 0:  # Première verticale_line
                line["x0"] = line["x1"] = next_vertical_lines[0]["x0"]
            elif j == len(vertical_lines) - 1:  # Dernière verticale_line
                line["x0"] = line["x1"] = next_vertical_lines[-1]["x0"]
            else:  # Autres verticales_lines
                closest_x0 = min(
                    (vl["x0"] for vl in next_vertical_lines),
                    key=lambda x: abs(x - x0)
                )
                line["x0"] = line["x1"] = closest_x0

        all_lines.extend(vertical_lines)

    return all_lines



def get_lines_stream_v2(tables:camelot.core.TableList, page, page_number, pdf_path)->list:
        """Get the coordinates of lines (of an axis) used by camelot to extract a table with Stream

        Args:
            tables (pdfplumber.core.TableList): a pdfplumber table
            axis (int): the axis of the target lines (0 for row, 1 for column)

        Returns:
            list: list of lines
        """

        all_vertical_lines = [0, 0]
        for _, table in enumerate(tables):
            index_headers, row_areas = get_index_headers_and_row_areas(table, page, page_number, pdf_path)
            table_areas = extract_areas(row_areas, index_headers)
            unsnapped_vertical_lines = get_vertical_lines_from_camelot(table_areas, page, page_number, pdf_path)
            # [{area_coords:"coords", area_type:"alone", vertical_lines:[[top,etc], ... ]}, {...}]
            snapped_vertical_lines = snap_vertical_lines(unsnapped_vertical_lines) # voir si alone et s'adapte à celui d'après
            all_vertical_lines.extend(snapped_vertical_lines)
            
        return all_vertical_lines


def get_lines_stream(tables:camelot.core.TableList, axis:int)->list:
        """Get the coordinates of lines (of an axis) used by camelot to extract a table with Stream

        Args:
            tables (camelot.core.TableList): a camelot table
            axis (int): the axis of the target lines (0 for row, 1 for column)

        Returns:
            list: list of lines
        """
        lines = [0, 1]
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

def extract_tables_page_v2(page:pdfplumber.page.Page, page_number:int,pdf_path:str,
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
    
    text_axes = np.where(np.array(methods) == 'explicit')[0]

    lines = {0:[], 1:[]}
    if methods[0] != "explicit" and methods[1] == "explicit":
        init_settings = {"vertical_strategy": "text", "horizontal_strategy": "lines"}
        tables = page.find_tables(init_settings)
        lines[1] = get_lines_stream_v2(tables, page, page_number, pdf_path)

    elif len(text_axes > 0):
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