import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards

file_path="E:/perso/Année scolaire 2024-2025/Cours/PIP/Projet-Interpromo-Groupe-1/data/transformed/EDF/"
df = pd.read_csv(file_path+"effectif/effectif.csv", sep=";")

#---------------Checkbox pour choisir les axes d'analyse

col_quali = df.select_dtypes(include=["object", "category"]).columns.tolist()
col_quali.append("Année")
col_z = st.sidebar.selectbox("Indicateur :", col_quali, index=1) 
df_grouped = df.groupby([col_z], as_index=False).sum()

#-------------CREATION DES GRAPHIQUES--------------

fig_bar=px.bar(df, x=col_z, y="Valeur",
            labels={"Année": "Année", "Valeur":"Effectif"},
            title="Effectif des employés par année"
            )

#  graphique en anneau
fig_donut = px.pie(df, names=col_z, values="Valeur", 
                   title="Effectif des employés par année", hole=0.6)

# graphique boxplot
fig_box = px.box(df, x="Année", y="Valeur", color="Année",
                 title="Effectif des employés par année")

# graphique violon
fig_violin = px.violin(df, x="Année", y="Valeur", color="Année", box=True,
                 points="all", title="Effectif des employés par année")



##------------------AFFICHAGE PRINCIPAL----------------------------##
st.title("Analyse univarié")
#---------Affichage de statistiques------------------
col1, col2,col3 = st.columns(3)
#col3, col4 = st.columns(2)

col1.metric("Minimum", int(df["Valeur"].min()), border=True)
col2.metric("Moyenne", int(df["Valeur"].mean()), border=True)
col3.metric("Maximum", int(df["Valeur"].max()), border=True)
style_metric_cards(border_left_color= "#FFDD99")

#-------------AFFICHAGE DES GRAPHIQUES--------------
#Boite à cocher
choix_graph = st.radio( "", ["Répartition", "Dispersion"],  index=0,
                       horizontal=True)

#Les graphs pour analyser la répartition---------------------------------
a,b=st.columns(2)
if choix_graph=="Répartition": #description repartition
    with a: 
        st.divider()
        st.plotly_chart(fig_donut)

           #st.divider()
        #st.plotly_chart(fig_pie)

    with b: #description simple
        st.divider()
        st.plotly_chart(fig_bar)

#Les graphs pour analyser la dispersion---------------------------------
elif choix_graph=="Dispersion" :
    c,d=st.columns(2) 
    with c:
        st.divider()
        st.plotly_chart(fig_box) #trouver les points abbérants

    with d:
        st.divider()
        st.plotly_chart(fig_violin) #montrer la densité des données et leur distribution


