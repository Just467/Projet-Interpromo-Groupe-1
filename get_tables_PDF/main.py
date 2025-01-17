import pdfplumber
import sys
sys.path.append('get_tables_PDF')
from function_get_tables_PDF import get_all_raw_tables_PDF
from extract_tables_PDF_page import extract_tables_page, extract_tables_page_v2
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

test1 = {'CNP':{'path':r'data\bilans_sociaux\CNP-Assurances-Bilan-social-2023.pdf',
                              'extract_settings': {},
                              'methods':['lines', 'explicit'],
                              'pattern': r'[IV]+\.\d+\.?\d* - '}}

test2 = {'ENGIE':{'path':r'data\bilans_sociaux\ENGIE SA_Bilan social 2021_VD.pdf',
                              'extract_settings': {},
                              'methods':['lines', 'lines'],
                              'pattern': r'\d{3}\. +'}}

results = get_all_raw_tables_PDF(test1['CNP'], pages = [19],
                                 save=False, save_folder_path=r"data\transformed\CNP",
                                 pivot=False,
                                 extract_tables_page_function=extract_tables_page_v2)
tables = []
headers = []
for result in results:
    tables.append(result['table'])
    headers.append(f"{result['title']}\n{result['pages']}")
show_dataframes(tables, headers=headers)