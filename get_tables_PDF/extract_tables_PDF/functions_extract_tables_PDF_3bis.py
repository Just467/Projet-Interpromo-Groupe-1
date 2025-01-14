import camelot
import pandas as pd
import pdfplumber

# Constants for supported table extraction methods
EXTRACT_TABLES_PDF_METHODS = ['lines', 'lines_strict', 'explicit']
def extract_table_areas(rows, index_headers, index_nan):
    """
    Extract table areas by grouping rows until encountering a header or NaN.

    Args:
        rows (list): List of (x1, y1, x2, y2) coordinates for each row.
        index_headers (list): Indices of rows that are headers.
        index_nan (list): Indices of rows that are NaN.

    Returns:
        list: List of table areas as (x1, y1, x2, y2).
    """
    areas = []  # To store table areas
    i = 0

    while i < len(rows):
        if i in index_nan:
            i += 1
            continue

        # Start a new area with the current row's coordinates
        current_area = rows[i]

        # Traverse subsequent rows until encountering a header or NaN
        while (
            i + 1 < len(rows)
            and i + 1 not in index_headers
            and i + 1 not in index_nan
        ):
            i += 1
            current_area[2:] = rows[i][2:]

        areas.append(current_area)
        i += 1

    return areas
    
def has_row_nan(index, tables):
    """
    Vérifie si une ligne Camelot est constituée uniquement de cellules vides ou None.

    Args:
        row_camelot (list): Liste des cellules d'une ligne Camelot.

    Returns:
        bool: True si toutes les cellules sont vides ou None, sinon False.
    """
    for table in tables:
        for _, row in enumerate(table.cells):
            for cell in row:
                if not(cell is None or cell.text is None or cell.text.strip() == "" or cell.text.strip() == "\n"):
                       return False
    return  True

import re

def has_header_row(tables, min_year=2020, max_year=2025):
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



def get_vertical_lines_from_camelot(tables, top_coord, bottom_coord):
    """
    Extract vertical lines as objects from Camelot tables.

    Args:
        tables (camelot.core.TableList): List of tables detected by Camelot.
        top_coord (float): Top coordinate of the row.
        bottom_coord (float): Bottom coordinate of the row.

    Returns:
        list: Vertical lines formatted as pdfplumber-compatible objects.
    """
    vertical_lines = []
    for table in tables:
        for row in table.cells:
            nb_cells = len(row)
            for cell_index in range(nb_cells):
                cell = row[cell_index]

                # Right edge of the current cell
                vertical_lines.append({
                    "x0": cell.x1,
                    "x1": cell.x1,
                    "top": top_coord,
                    "bottom": bottom_coord,
                    "height": bottom_coord - top_coord,
                    "orientation": "v",
                    "object_type": "line"
                })

                # Add the right edge of the last cell
                if cell_index == nb_cells - 1:
                    vertical_lines.append({
                        "x0": cell.x2,
                        "x1": cell.x2,
                        "top": top_coord,
                        "bottom": bottom_coord,
                        "height": bottom_coord - top_coord,
                        "orientation": "v",
                        "object_type": "line"
                    })
    return vertical_lines

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

def find_first_horizontal_line(area, offset):
    first_horizontal_line = {
        "x0": area[0],
        "x1": area[3],
        "top": area[1]+offset,
        "bottom": area[1]+offset,
        "width": area[3] - area[0],
        "orientation": "h",
        "object_type": "line"
    }

    return first_horizontal_line



def complete_extract_tables_PDF(pdf_path, page, page_number, settings, methods, show_debugging=False):
    """
    Extract tables from a PDF page using Camelot and pdfplumber.

    Args:
        pdf_path (str): Path to the PDF file.
        page (pdfplumber.page.Page): PdfPlumber page object.
        page_number (int): The page number (0-indexed).
        settings (dict): Settings for pdfplumber's `extract_tables`.
        methods (list): Extraction methods for rows and columns.
        show_debugging (bool): Whether to show pdfplumber debugging visuals.

    Returns:
        list: A list of pandas DataFrames for each detected table.
    """
    page_height = page.height

    # Initialize settings for pdfplumber's table detection
    init_settings = {
        "vertical_strategy": "text",
        "horizontal_strategy": "lines"
    }
    
    # Detect tables using pdfplumber
    tables = page.find_tables(init_settings)
    vertical_lines = []
    horizontal_lines = []

    for table in tables:
        index_headers = []
        index_nan = []
        rows = []
        for index, row in enumerate(table.rows):
            try:
                row_coords = get_row_coords(row.cells)
                rows.append(row_coords)
                str_row_area = get_table_area(row_coords, page_height)

                row_camelot = camelot.read_pdf(
                    pdf_path,
                    flavor="stream",
                    pages=f"{page_number + 1}",
                    table_areas=[str_row_area],
                    flag_size=True
                )

                if has_header_row(row_camelot):
                    index_headers.append(index)
                
                if has_row_nan(index, row_camelot):
                    index_nan.append(index)

            except ValueError as e:
                print(f"Skipping row due to error: {e}")
                index_nan.append(index)
            except Exception as e:
                print(f"Unexpected error: {e}")


        try:
            table_areas_list = extract_table_areas(rows, index_headers, index_nan)
            offset = -30
            a, b, c, d = table_areas_list[0]
            new_area = [a, b + offset, c, b]
            new_horizontal_line = {
                "x0": a,
                "x1": c,
                "top": b + offset,
                "bottom": b + offset,
                "width": c - a,
                "orientation": "h",
                "object_type": "line"
            }
            table_areas_list.extend([new_area])
            horizontal_lines.extend([new_horizontal_line])
            for area_coords in table_areas_list:
                print(area_coords)
                str_area = get_table_area(area_coords, page_height)

                row_camelot = camelot.read_pdf(
                    pdf_path,
                    flavor="stream",
                    pages=f"{page_number + 1}",
                    table_areas=[str_area]
                )

                top_row, bottom_row = area_coords[1], area_coords[3]
                row_vertical_lines = get_vertical_lines_from_camelot(row_camelot, top_row, bottom_row)
                vertical_lines.extend(row_vertical_lines)

        except ValueError as e:
            print(f"Skipping row due to error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    if len(vertical_lines) >= 2:
            settings.update({
                "horizontal_strategy": methods[0],
                "vertical_strategy": methods[1],
                "explicit_vertical_lines": vertical_lines,
                "snap_x_tolerance": 10
            })
    if len(horizontal_lines) > 0:
            settings.update({
                "explicit_horizontal_lines": horizontal_lines
            })

    # Extract tables using updated settings
    extracted_tables = page.extract_tables(settings)
    df_tables = [pd.DataFrame(table) for table in extracted_tables]

    # Optional: Display debugging visuals
    if show_debugging:
        page.to_image().debug_tablefinder(settings).show()

    return df_tables