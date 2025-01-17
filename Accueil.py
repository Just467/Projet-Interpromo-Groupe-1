import streamlit as st
from PIL import Image
import streamlit_extras
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.switch_page_button import switch_page

# ---------- Page Configuration ----------
st.set_page_config(
    page_title="Page d'accueil - Comparaison des indicateurs",
    page_icon="📊",
    layout="wide"
)
button_style = """button{
    opacity: 0  ;
    padding-top: 50%;
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
# ---------- Page Title ----------
imgtit = Image.open("images/logos.png")  
left_co, cent_co,last_co = st.columns(3)
with last_co:
    st.image(imgtit, width=300)
st.write('')
st.title("Analyse de diversité et inclusion chez EDF et entreprises comparables")
st.markdown("## PIP 2025 - Groupe 1")
# ---------- Section: Logos avec boutons cliquables ----------
st.markdown("### Sélectionnez une entreprise pour explorer ses indicateurs")

# Logos des entreprises 
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    with stylable_container( key="r_buton", css_styles= button_style):
        details_bouton= st.button("texte", key='entreprise 1', use_container_width= True)
    img1 = Image.open("images/EDF.png")  
    st.image(img1, use_container_width=True)
    if details_bouton:
        switch_page("EDF")

with col2:
    with stylable_container( key="r_buton", css_styles= button_style):
        details_bouton= st.button("texte", key='entreprise 2', use_container_width= True)
    img2 = Image.open("images/engie-logo-0.png")  
    st.image(img2, use_container_width=True)
    if details_bouton:
        switch_page("ENGIE")

with col3:
    with stylable_container( key="r_buton", css_styles= button_style):
        details_bouton= st.button("texte", key='entreprise 3', use_container_width= True)
    img3 = Image.open("images/Deca.png")  
    st.image(img3, use_container_width=True)
    if details_bouton:
        switch_page("DECATHLON")


with col4:
    with stylable_container( key="r_buton", css_styles= button_style):
        details_bouton= st.button("texte", key='entreprise 4', use_container_width= True)
    img4 = Image.open("images/insa.png")  
    st.image(img4, use_container_width=True)
    if details_bouton:
        switch_page("INSA")

   
   
with col5:
    with stylable_container( key="r_buton", css_styles= button_style):
        details_bouton= st.button("texte", key='entreprise 5', use_container_width= True)
    img5 = Image.open("images/CNP-Logo.jpg")  
    st.image(img5, use_container_width=True)
    if details_bouton:
        switch_page("CNP")

container_style = """
{   
    z-index : 0;
    background-color: #F0F2F6;
    border: 2px solid #000000;
    padding-left: 150px;
    padding-top: 10px;
    padding-bottom:20px;
    border-radius: 20px;

}
"""

with stylable_container( key="r_buton", css_styles= button_style):
    details_bouton= st.button("texte", key='comparaison', use_container_width= True)
with stylable_container(
    key="button_comp",
    css_styles=container_style,
):
    button = st.container()
    if details_bouton :
        switch_page('COMPARAISON')
    button.markdown('<p style = "font-weight: 700; vertical-align: middle; font-family: system-ui; color: #000000; font-size: 40px;">Comparer EDF avec les autres entreprises</p>', unsafe_allow_html=True)
