import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from streamlit_extras.dataframe_explorer import dataframe_explorer 


file_path="E:/perso/Année scolaire 2024-2025/Cours/PIP/Projet-Interpromo-Groupe-1/data/transformed/EDF/"
df = pd.read_csv(file_path+"effectif/effectif.csv", sep=";")

#Mettre un filtre en haut de la table


st.write("1- Visualisation de la data")
filtered_df = dataframe_explorer(df, case=False)
st.dataframe(df,use_container_width=True)
