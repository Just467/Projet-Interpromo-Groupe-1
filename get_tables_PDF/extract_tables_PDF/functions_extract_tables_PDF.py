import camelot
import pandas as pd
import numpy as np
import pdfplumber

extract_tables_PDF_methods = ['lines', 'lines_strict', 'explicit']

def complete_extract_tables_PDF(pdf_path:str,
                                page:pdfplumber.page.Page, page_number:int, settings:dict,
                                methods:list,
                                show_debugging:bool=False):
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
    
    def get_lines_stream(tables:camelot.core.TableList, axis:int):
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
    
    text_axes = np.where(np.array(methods) == 'explicit')[0]
    lines = {0:[], 1:[]}
    if any(text_axes):
        tables = camelot.read_pdf(pdf_path, flavor="stream", pages=f"{page_number+1}")
        for text_axis in text_axes:
            lines[text_axis] = get_lines_stream(tables, text_axis)
    
    settings["horizontal_strategy"], settings["vertical_strategy"] = methods[0], methods[1]
    settings["explicit_horizontal_lines"], settings["explicit_vertical_lines"] = lines[0], lines[1]
    
    all_tables = page.extract_tables(settings)
    df_tables = [pd.DataFrame(table) for table in all_tables]
    if show_debugging:
        page.to_image().debug_tablefinder(settings).show()
    return df_tables
