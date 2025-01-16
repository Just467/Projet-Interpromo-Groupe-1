import streamlit as st
import pandas as pd
import numpy as np
from tempfile import NamedTemporaryFile
from streamlit_extras.stylable_container import stylable_container 
from streamlit_extras.switch_page_button import switch_page
from streamlit_pdf_viewer import pdf_viewer
from get_tables_PDF.function_get_tables_PDF import get_all_raw_tables_PDF

## Page style ##

st.set_page_config(
     page_title = 'Scraper de bilans sociaux',
     page_icon = 'page_facing_up',
     layout = 'wide',
     initial_sidebar_state = 'collapsed'
)

st.title("PDF scraper pour les bilans sociaux")

## PDF Upload ##

uploaded_pdf = st.file_uploader('Choisir ou glisser un fichier .pdf', type='pdf',accept_multiple_files=False)

def uploaded_to_binary(uploaded_file) :
    binary = uploaded_pdf.getvalue()
    tmp_file = NamedTemporaryFile()
    tmp_file.write(bytearray(binary))
    return (binary)
b_pdf = uploaded_to_binary(uploaded_pdf)
try:
    pass
except:
    b_pdf = None
import io
result = get_all_raw_tables_PDF({'path':io.BytesIO(b_pdf),
                                'extract_settings': {},
                                'methods':['lines', 'lines'],
                                'pattern': r''},
                                pages=[15]
                                )
print(result[0])


## DF to csv for the download

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


## columns 

col1, col2, col3, col4 = st.columns([1,2,2,1])
with col2 :
    if b_pdf is not None :
        page = st.selectbox(label='Page', options=list(range(1,10)))
        if page is not None :
            pdf_viewer(b_pdf, pages_to_render=[page])
        else :
            pdf_viewer(b_pdf, pages_to_render=[1])
with col3 :
    if b_pdf is not None :
        df = pd.DataFrame(np.reshape(np.zeros(100), [10,10]))
        edited_df = st.data_editor(df, use_container_width=True)
        csv = convert_df(edited_df)
        st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name="table_data.csv",
        mime="text/csv",
        use_container_width=True
    )

