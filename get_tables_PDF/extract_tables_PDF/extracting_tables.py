import camelot
import pdfplumber
import pandas as pd
import sys
sys.path.append('get_tables_PDF')
from utils.table_viewer import show_table
from extract_tables_PDF.functions_extract_tables_PDF import merge_stream_pdfplumber

page_number = 17

with pdfplumber.open(r"data\bilans_sociaux\CNP-Assurances-Bilan-social-2023.pdf") as pdf:
    settings = {}
    page = pdf.pages[page_number]
    pdfplumber_df = pd.DataFrame(page.extract_table(settings))
pdfplumber_df = pdfplumber_df.head(10)

stream_tables = camelot.read_pdf(r"data\bilans_sociaux\CNP-Assurances-Bilan-social-2023.pdf", flavor="stream", pages=f'{page_number+1}')
stream_df = stream_tables[0].df

df = merge_stream_pdfplumber(pdfplumber_df, stream_df)
df.columns = df.columns.astype(str)
show_table(df)