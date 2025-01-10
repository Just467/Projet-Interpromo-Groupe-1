import streamlit as st
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