import pdfplumber
import sys
sys.path.append('get_tables_PDF')
from extract_tables_PDF.functions_extract_tables_PDF import complete_extract_tables_PDF
from utils.dataframe_viewer import show_dataframes

paths = [
    r'data\bilans_sociaux\CNP-Assurances-Bilan-social-2023.pdf',
    r'data\bilans_sociaux\ENGIE SA_Bilan social 2021_VD.pdf',
    r'data\bilans_sociaux\INSA_bilan_soc_20_V2_21.pdf'
]

page_number = 10
settings = {
}

with pdfplumber.open(path3) as pdf:
    page = pdf.pages[page_number]
    result = complete_extract_tables_PDF(path3,
                                         page, page_number, settings,
                                         methods=['lines', 'lines'],
                                         show_debugging=True)
    print(result)
    show_dataframes(result)
    