# p2_dataframe_demo

import streamlit as st
import pandas as pd
import numpy as np

st.write('# Data')

col1, col2 = st.columns(2)

with col1:
    entreprise = st.radio(
        "Choisissez une entreprise",
        key="entreprise",
        options=["EDF", "CNP", "ENGIE", "INSA", "Decathelon"],
    )

with col2:
    option = st.selectbox(
        "Veuillez choisir une thématique",
        ("Genre", "Age", "Handicap"),
        index=None,
        placeholder="Sélectionnez une thématique...",
    )
if entreprise == 'EDF' and option == 'Handicap':
    df_edf_handi = pd.read_csv('C:\\Users\\Admin\\Documents\\AS 2024 2025\\Deuxième semestre\\Projet inter-promo\\bilan-social-d-edf-sa-salaries-en-situation-de-handicap.csv', sep=';')
    df_edf_handi = df_edf_handi.drop(['Perimètre juridique', 'Perimètre spatial','Spatial perimeter','Indicator','Type of contract','Employee category','Gender','Unit','Chapitre du bilan social','Unité'], axis=1)
    st.write(df_edf_handi)
