import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import os 
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container
# Mise en forme avec Streamlit Extras pour ajouter des bordures, etc.
import streamlit_extras 

from utils import selection_menu, titre, mise_en_forme_graph  #, affichage_graphs

st.set_page_config(layout="wide")  # Utiliser toute la largeur de l'écran


##############################################################
#--########-------CREATION DES GRAPHIQUES----######
##############################################################

def affichage_graphs (selection, indicateur_, df, dimension_1, dimension_2):
    """Fonction qui prends en paramètres la ou les thématiques, l'indicateur choisi, les données en lien et les axes d'analyse choisis
    et qui retourne l'affichage de l'ensembles des graphiques."""

    #----------------Graph univarié-----------------------------
    if selection and indicateur_ and dimension_1 and not dimension_2:
        df_grouped = df.groupby(["Année",dimension_1], as_index=False).sum()

        fig_ligne=px.line(df_grouped, x="Année",
                        y="Valeur",
                        color=dimension_1,
                        labels={dimension_1, "Valeur: "+indicateur_},
                        markers=True,
                        # title="Evolution des "+ indicateur_+ "des employés par année",
                        color_discrete_sequence=px.colors.qualitative.D3
                        )
        fig_bar=px.bar(df_grouped, x="Année",
                y="Valeur",
                color=dimension_1,
                barmode="group",
                labels={dimension_1, "Valeur: "+indicateur_},
                #title="Evolution des "+ indicateur_+ "des employés par année",
                color_discrete_sequence=px.colors.qualitative.D3 )

        a,b=st.columns(2)
        with a:
            mise_en_forme_graph (fig_bar, "graph_containera", indicateur_)
        with b:
            mise_en_forme_graph (fig_ligne, "graph_containerb", indicateur_)
    elif selection and indicateur_ and dimension_1:
    #----------------Graph multiple----------------------------

        df_grouped = df.groupby(["Année",dimension_1,dimension_2], as_index=False).sum()
        fig_secteur = px.sunburst(df_grouped, path=["Année",dimension_1,dimension_2], values="Valeur")
                        # title=indicateur_+ " des employés par année"
        fig_multi_lignes = px.line(df_grouped, x="Année", y="Valeur", 
                                    color=dimension_1, line_dash=dimension_2,
                                    markers=True)

        col1, col2 = st.columns(2)

        # Colonne 1 : Secteur 
        with col1:
            mise_en_forme_graph (fig_secteur, "graph_container1", indicateur_)

        # Colonne 2 : Multi-lignes
        with col2:
            mise_en_forme_graph (fig_multi_lignes, "graph_container2", indicateur_)

### Appel de la fonction ###

dossier_entreprise = "../data/transformed/EDF/"
col_inutiles = ["Perimètre juridique","Perimètre spatial","Chapitre du bilan social","Unité","Plage M3E"]
selection, indicateur_, df, dimension_1, dimension_2 = selection_menu(dossier_entreprise,col_inutiles)
affichage_graphs (selection, indicateur_, df, dimension_1, dimension_2)









