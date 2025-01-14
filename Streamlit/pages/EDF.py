import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import os 
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container
# Mise en forme avec Streamlit Extras pour ajouter des bordures, etc.
import streamlit_extras 
from utils import selection_menu , affichage_graphs

st.set_page_config(layout="wide")  # Utiliser toute la largeur de l'écran


##############################################################
#--########-------CREATION DE LA PAGE EDF----######
##############################################################

### Appel de la fonction ###

dossier_entreprise = "..\\data\\transformed\\EDF"
col_inutiles = ["Perimètre juridique","Perimètre spatial","Chapitre du bilan social","Unité","Plage M3E"]
selection, indicateur_, df, dimension_1, dimension_2 = selection_menu(dossier_entreprise,col_inutiles)
affichage_graphs (selection, indicateur_, df, dimension_1, dimension_2)









