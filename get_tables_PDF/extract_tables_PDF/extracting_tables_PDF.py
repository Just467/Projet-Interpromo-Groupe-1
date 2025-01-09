import pdfplumber
import sys
sys.path.append('get_tables_PDF')
from extract_tables_PDF.functions_extract_tables_PDF import complete_extract_tables_PDF

path = r'data\bilans_sociaux\CNP-Assurances-Bilan-social-2023.pdf'
page_number = 17
with pdfplumber.open(path) as pdf:
    page = pdf.pages[page_number]
    result = complete_extract_tables_PDF(path,
                                         page, page_number,
                                         methods=['lines', 'explicit'],
                                         show_debugging=True)
    print(result)