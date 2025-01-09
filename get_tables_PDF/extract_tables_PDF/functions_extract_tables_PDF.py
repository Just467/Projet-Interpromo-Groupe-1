import camelot
import pandas as pd
import numpy as np

extract_tables_PDF_methods = ['lines', 'lines_strict', 'explicit']

def complete_extract_tables_PDF(pdf_path,
                       page, page_number,
                       methods,
                       show_debugging=False):
    if methods[0] not in extract_tables_PDF_methods or methods[1] not in extract_tables_PDF_methods:
        raise ValueError(f"Both values of methods must be in {", ".join([str(elem) for elem in extract_tables_PDF_methods])}")
    
    def get_lines_stream(tables, axis):
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
    
    settings = {"horizontal_strategy": methods[0],
                "vertical_strategy": methods[1],
                "explicit_horizontal_lines": lines[0],
                "explicit_vertical_lines": lines[1]}
    
    df_table = pd.DataFrame(page.extract_table(settings))
    if show_debugging:
        page.to_image().debug_tablefinder(settings).show()
    return df_table
