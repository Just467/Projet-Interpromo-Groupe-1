import streamlit as st
import pandas as pd  
import plotly.express as px 
from PIL import Image
import streamlit_extras
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.switch_page_button import switch_page
button_style = """button{
    opacity: 0;
    padding-top: 100%;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 1;
    margin: 0;
    float: none;
}
"""
container_style = """{
    z-index: 0;
    background_color: #171717;
    border-top: 2px solid #373737;
}
"""

col1, col2, col3 = st.columns(3)


with col1:
    with stylable_container( key="r_buton", css_styles= button_style):
        details_bouton= st.button("texte", key='entreprise 1', use_container_width= True)
    img1 = Image.open("/home/sid2018-3/Téléchargements/Logo-EDF.png")
    st.image(img1, use_container_width=True)
    if details_bouton:
        switch_page("EDF")

with col2:
    with stylable_container( key="r_buton", css_styles= button_style):
        details_bouton= st.button("texte", key='entreprise 2', use_container_width= True)
    img2 = Image.open("/home/sid2018-3/Téléchargements/800px-ENGIE_logotype_2018.png")
    st.image(img2, use_container_width=True)
    if details_bouton:
        switch_page("ENGIE")

with col3:
    with stylable_container( key="r_buton", css_styles= button_style):
        details_bouton= st.button("texte", key='entreprise 3', use_container_width= True)
    img3 = Image.open("/home/sid2018-3/Téléchargements/logo-decathlon-bleu-1280x720.webp")
    st.image(img3, use_container_width=True)
    if details_bouton:
        switch_page("DECATHLON")

# chargement des fichiers

# absentésime
