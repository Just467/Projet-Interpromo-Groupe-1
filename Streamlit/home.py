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
# ---------- Page Title ----------
st.title("📊 Analyse et comparaison des indicateurs d'entreprises")

# ---------- Section: Logos avec boutons cliquables ----------
st.markdown("### Sélectionnez une entreprise pour explorer ses indicateurs:")

# Logos des entreprises (exemple avec 3 entreprises)
col1, col2, col3 = st.columns(3)

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
# ---------- Section: Comparaison entre entreprises ----------
st.markdown("### Comparer deux entreprises sur un indicateur :")


# Sélection des entreprises à comparer
company_list = ["EDF", "ENGIE", "DECATHLON"]
selected_companies = st.multiselect("Choisir les entreprises à comparer", company_list)

 # Validation des entreprises sélectionnées
if len(selected_companies) == 2:
    if st.button("Valider la sélection"):
        st.session_state["comparison"] = selected_companies
        switch_page("M_COMPARAISON")
else:
    st.info("Veuillez sélectionner exactement deux entreprises pour continuer.")

   
import pandas as pd 
import plotly.express as px 

# menu déroulant 

entreprises = ["EDF", "ENGIE", "INSA", "DECATHLON","CNP"]
selected_entreprises = []

# Afficher les cases à cocher
st.subheader("Cochez les entreprises de votre choix: ")

for entreprise in entreprises:
    if st.checkbox(entreprise, key=entreprise):
        selected_entreprises.append(entreprise)
    
# Confirmer la sélection
if st.button("Valider la sélection"):
    if selected_entreprises:
        st.success("Vous avez sélectionné: " + ",".join(selected_entreprises))
    else:
        st.warning("Aucune entreprise n'a été sélectionnée")
