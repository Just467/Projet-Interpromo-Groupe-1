import pdfplumber
import sys
sys.path.append('get_tables_PDF')
from get_tables_PDF.extract_tables_PDF_page import get_all_raw_tables_PDF
from utils.dataframe_viewer import show_dataframes

bilan_sociaux_paths = {'CNP':{'path':r'data\bilans_sociaux\CNP-Assurances-Bilan-social-2023.pdf',
                              'extract_settings': {},
                              'methods':['lines', 'explicit'],
                              'pattern': r'I+\.\d+\.?\d* - '},
                       'ENGIE':{'path':r'data\bilans_sociaux\ENGIE SA_Bilan social 2021_VD.pdf',
                              'extract_settings': {},
                              'methods':['lines', 'lines'],
                              'pattern': r'\d{3}\. +'},
                       'INSA':{'path':r'data\bilans_sociaux\INSA_bilan_soc_20_V2_21.pdf',
                              'extract_settings': {},
                              'methods':['lines', 'lines'],
                              'pattern': r''}
                       }

test = {'CNP':{'path':r'data\bilans_sociaux\CNP-Assurances-Bilan-social-2023.pdf',
                              'extract_settings': {},
                              'methods':['lines', 'explicit'],
                              'pattern': r'I+\.\d+\.?\d* - '}}

test = {'ENGIE':{'path':r'data\bilans_sociaux\ENGIE SA_Bilan social 2021_VD.pdf',
                              'extract_settings': {},
                              'methods':['lines', 'lines'],
                              'pattern': r'\d{3}\. +'}}

result = get_all_raw_tables_PDF(test, pages = [25])
print(f"Résultat\n{result['ENGIE']}")        
    