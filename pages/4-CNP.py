import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import os 
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container
# Mise en forme avec Streamlit Extras pour ajouter des bordures, etc.
import streamlit_extras 
from PIL import Image

from utils import importation_data, selection_menu, affichage_graphs

st.set_page_config(layout="wide")  # Utiliser toute la largeur de l'écran
imgtit = Image.open("images/logos.png")  
left_co, cent_co,last_co = st.columns(3)
with last_co:
    st.image(imgtit, width=300)
st.write('')
st.title("Diversité et inclusion chez CNP")
### Appel de la fonction ###

dossier_entreprise = "data/transformed/CNP"
col_inutiles = ["Perimètre juridique","Perimètre spatial","Chapitre du bilan social"]
selection, resultats, liste_indicateurs = importation_data (dossier_entreprise, col_inutiles)
if selection:
    selection, indicateur_, df, dimension_1, dimension_2 = selection_menu(selection, resultats, liste_indicateurs)
    affichage_graphs (selection, indicateur_, df, dimension_1, dimension_2)










