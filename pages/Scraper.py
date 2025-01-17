import io
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_extras.stylable_container import stylable_container 
from streamlit_extras.switch_page_button import switch_page
from streamlit_pdf_viewer import pdf_viewer
from tempfile import NamedTemporaryFile
from get_tables_PDF.function_get_tables_PDF import get_all_raw_tables_PDF
from get_tables_PDF.extract_tables_PDF_page import extract_tables_page, extract_tables_page_v2


def uploaded_to_binary(uploaded_file) :
    binary = uploaded_file.getvalue()
    tmp_file = NamedTemporaryFile()
    tmp_file.write(bytearray(binary))
    return (binary)


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(sep = ';').encode("iso-8859-1")

@st.fragment
def show_extrated_tables(extracted_tables, page_number):
    st.markdown("""<p style='font-size:20px;'>Choisir une table</p>""",
                unsafe_allow_html=True)
    select_box = st.selectbox(label='',
                              options=[i for i in range(len(extracted_tables))],
                              format_func=lambda x: "Table n°"+str(x+1), label_visibility='collapsed')
    try:
        # get index of table
        st.session_state.df_selector = select_box
        # get table
        edited_df = st.data_editor(extracted_tables[st.session_state.df_selector]['table'], use_container_width=True)
        csv = convert_df(edited_df)
        st.markdown("""<p style='font-size:20px;'>Choisir un titre pour le fichier CSV</p>""",
                unsafe_allow_html=True)
        csv_title = st.text_input(
            label="",
            value=f"page_{page_number}_table_{st.session_state.df_selector+1}",
            label_visibility='collapsed')  
        st.download_button(
            label="Download table as CSV",
            data=csv,
            file_name=csv_title+'.csv',
            mime="text/csv",
            use_container_width=True)
    except:
        pass


# Page style
st.set_page_config(
     page_title = 'Scraper de bilans sociaux',
     page_icon = 'page_facing_up',
     layout = 'wide',
     initial_sidebar_state = 'collapsed'
)



## Ttitle ##
st.title("PDF scraper pour les bilans sociaux")

## PDF Upload ##
uploaded_pdf = st.file_uploader('Choisir ou glisser un fichier .pdf', type='pdf',accept_multiple_files=False)
try:
    b_pdf = uploaded_to_binary(uploaded_pdf)
except:
    b_pdf = None

## PDF page ##
page_number = st.number_input('Choisir le numéro de la page', value=0)

## Confirm Button ##
confirm_button = st.button('Confirm')

## Columns ##
col1, col2, col3, col4 = st.columns([1,32,32,1])

extracted_tables = []   

if b_pdf and page_number and confirm_button:
    try:
        del st.session_state.df_selector
    except:
        pass
    extracted_tables = get_all_raw_tables_PDF({'path':io.BytesIO(uploaded_pdf.getvalue()),
                                               'extract_settings': {},
                                               'methods':['lines', 'explicit'],
                                               'pattern': r''},
                                               pages=[page_number-1],
                                               final_tables=[],
                                               pivot=False,
                                               extract_tables_page_function=extract_tables_page_v2)
if 'df_selector' not in st.session_state:
    st.session_state.df_selector = 0


with col2:
    if b_pdf and page_number:
        pdf_viewer(b_pdf, pages_to_render=[page_number], width=100000)
with col3:
    show_extrated_tables(extracted_tables, page_number)
