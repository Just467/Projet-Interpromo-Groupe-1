import pdfplumber
import sys
sys.path.append('get_tables_PDF')
from extract_tables_PDF.functions_extract_tables_PDF import get_all_raw_tables_PDF
from utils.dataframe_viewer import show_dataframes

bilan_sociaux_paths = {'CNP':{'path':r'data\bilans_sociaux\CNP-Assurances-Bilan-social-2023.pdf',
                              'extract_settings': {},
                              'methods':['lines', 'explicit']},
                       'ENGIE':{'path':r'data\bilans_sociaux\ENGIE SA_Bilan social 2021_VD.pdf',
                              'extract_settings': {},
                              'methods':['lines', 'lines']},
                       'INSA':{'path':r'data\bilans_sociaux\INSA_bilan_soc_20_V2_21.pdf',
                              'extract_settings': {},
                              'methods':['lines', 'lines']}
                       }

test = {'CNP':{'path':r'data\bilans_sociaux\CNP-Assurances-Bilan-social-2023.pdf',
               'extract_settings': {},
               'methods':['lines', 'explicit']}}

result = get_all_raw_tables_PDF(test, pages = [i for i in range(19)])
show_dataframes(result['CNP_title'])        
    