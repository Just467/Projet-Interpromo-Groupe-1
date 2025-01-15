import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

#Importation des données
file_path="E:/perso/Année scolaire 2024-2025/Cours/PIP/Projet-Interpromo-Groupe-1/data/transformed/EDF/"
df = pd.read_csv(file_path+"effectif/effectif.csv", sep=";")
st.title("Affichage des indicateurs")

st.divider()
st.subheader("Catégorie d'indicateur : Effectif")
st.markdown("Affichage des indicateurs liés à l'effectif des employés. Ce test se base sur les ficchiers d'EDF")



col_quali = df.select_dtypes(include=["object", "category"]).columns.tolist()
#Checkbox pour choisir les axes d'analyse
col_z = st.sidebar.selectbox("Indicateur :", col_quali, index=1) 

df_grouped = df.groupby(["Année",col_z], as_index=False).sum()

#st.write(df_grouped)
st.write("Page 3- Visualisation bidimensionnelle")
fig_line=px.line(df_grouped, x="Année",
             y="Valeur",
             color=col_z,
            labels={"Année": "Année", "Valeur":"Effectif"},
            title="Evolution des effectifs des employés par année",
            color_discrete_sequence=px.colors.qualitative.D3

            )
st.plotly_chart(fig_line)


# Afficher le graphique dans Streamlit
st.divider()