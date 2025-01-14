import pdfplumber
import sys
sys.path.append('get_tables_PDF')
from extract_tables_PDF.functions_extract_tables_PDF_3bis import complete_extract_tables_PDF
from utils.dataframe_viewer import show_dataframes

paths = [
    r'data\bilans_sociaux\CNP-Assurances-Bilan-social-2023.pdf'
]


settings = {
}

for page_number in range(100):
    with pdfplumber.open(paths[0]) as pdf:
        page = pdf.pages[page_number]
        result = complete_extract_tables_PDF(paths[0],
                                            page, page_number, settings,
                                            methods=['lines', 'explicit'],
                                            show_debugging=True)
        # show_dataframes(result)
    