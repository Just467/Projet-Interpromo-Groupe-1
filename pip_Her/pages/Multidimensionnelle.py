#https://plotly.streamlit.app/~/+/Figure_Factory_Subplots
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

file_path="E:/perso/Année scolaire 2024-2025/Cours/PIP/Projet-Interpromo-Groupe-1/data/transformed/EDF/"
df = pd.read_csv(file_path+"effectif/effectif.csv", sep=";")

#Prendre les variables qualitatives comme axe d'analyse
col_quali = df.select_dtypes(include=["object", "category"]).columns.tolist()

st.title("Analyse multivarié")
#---------------Checkbox pour choisir les axes d'analyse
choix_graph = st.multiselect("Type de graphique :", ["bar","ligne","secteur","empilé", "zone", "carte","treemap", "bulle"],
                             default=["carte"])
#filtre des axes d'analyse
col_z = st.sidebar.selectbox("Indicateur :", col_quali, index=1) 
df_grouped = df.groupby(["Année",col_z], as_index=False).sum()

#CREATION DES GRAPHS
tabs = []
figures = {}

if "secteur" in choix_graph: 
    figures["secteur"] = px.sunburst(df_grouped, path=["Année", col_z], values="Valeur",
                        title="Effectif des employés par année")
    tabs.append("secteur")

if "ligne" in choix_graph: 
    figures["ligne"]=px.line(df_grouped, x="Année",
                y="Valeur",
                color=col_z,
                labels={"Année": "Année", "Valeur":"Effectif"},
                title="Evolution des effectifs des employés par année",
                color_discrete_sequence=px.colors.qualitative.D3
                )
    tabs.append("ligne")

if "bar" in choix_graph: 
    figures["bar"]=px.bar(df_grouped, x="Année",
                y="Valeur",
                color=col_z,
                barmode="group",
                labels={"Année": "Année", "Valeur":"Effectif"},
                title="Evolution des effectifs des employés par année",
                color_discrete_sequence=px.colors.qualitative.D3

                )
    tabs.append("bar")

if "empilé" in choix_graph: 
    figures["empilé"]=px.bar(df_grouped, x="Année",
                y="Valeur",
                color=col_z,
                labels={"Année": "Année", "Valeur":"Effectif"},
                title="Evolution des effectifs des employés par année",
                color_discrete_sequence=px.colors.qualitative.D3

                )
    tabs.append("empilé")
# Créer la carte de chaleur
if "carte" in choix_graph: 
    map_data = df.pivot_table(values="Valeur", index="Année", columns=col_z, aggfunc="sum")

    figures["carte"] = px.imshow(
        map_data,
        text_auto=True,
        color_continuous_scale="Viridis",
        title="Carte des valeurs par Année et Genre")
    tabs.append("carte")

if "zone" in choix_graph: 
    figures["zone"] = px.area(
        df_grouped, 
        x="Année",
        y="Valeur",
        color=col_z,
        title="Graphique en zone"
    )
    tabs.append("zone")

if "treemap" in choix_graph: 
    figures["treemap"] = px.treemap(
        df_grouped, 
        path=["Année"], 
        values="Valeur", 
        title="Treemap"
    )
    tabs.append("treemap")

if "bulle" in choix_graph: 
    figures["bulle"]= px.scatter(df_grouped, x="Année", y="Valeur",
    size="Valeur", 
    color=col_z,
    log_x=True, size_max=37)
    tabs.append("bulle")


##------------------AFFICHAGE PRINCIPAL----------------------------##

if tabs:
    st_tabs = st.tabs(tabs)
    for i, tab in enumerate(st_tabs):
        with tab:
            st.plotly_chart(figures[tabs[i]])