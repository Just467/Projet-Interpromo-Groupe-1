import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import os
from utils import selection_menu, mise_en_forme_graph

# Sélectionner deux entreprises
entreprises = ["EDF", "ENGIE", "INSA", "DECATHLON", "CNP"]
selection = st.multiselect("Sélectionnez deux entreprises :", entreprises, default=None)

if len(selection) == 2:
    # Charger les données pour les entreprises sélectionnées
    dossier_entreprise1 = f"..\\data\\transformed\\{selection[0]}"
    dossier_entreprise2 = f"..\\data\\transformed\\{selection[0]}"

    col_inutiles = ["Perimètre juridique", "Perimètre spatial", "Chapitre du bilan social", "Unité", "Plage M3E"]

    # Charger les données pour chaque entreprise
    _, indicateur_1, df1, dimension_1, dimension_2 = selection_menu(dossier_entreprise1, col_inutiles)
    _, indicateur_2, df2, dimension_1, dimension_2 = selection_menu(dossier_entreprise2, col_inutiles)

    # Vérifier si les indicateurs sont communs
    indicateurs_communs = set(df1.columns).intersection(set(df2.columns))

    if indicateurs_communs:
        indicateur_commun = st.selectbox("Choisissez un indicateur commun :", list(indicateurs_communs))

        # Filtrer les données par l'indicateur commun
        df1_filtered = df1[df1["Indicateur"] == indicateur_commun]
        df2_filtered = df2[df2["Indicateur"] == indicateur_commun]

        # Afficher le graphique comparatif
        affichage_comparatif(selection, indicateur_commun, df1_filtered, df2_filtered, dimension_1, dimension_2)
    else:
        st.warning("Aucun indicateur commun trouvé entre les deux entreprises.")
else:
    st.warning("Veuillez sélectionner exactement deux entreprises pour effectuer une comparaison.")