import streamlit as st
import pandas as pd

opt_thm = ["Absentéisme","Autres conditions de travail","Droit du travail","Effectif et répartition par âge, statut et sexe","Formation","Rémunérations et promotions","Salariés en situation de handicap","Travailleurs extérieurs"]

selection = st.pills("Veuillez choisir une ou plusieurs thématiques à étudier :", opt_thm, selection_mode="multi")

match opt_thm:
    case "Absentéisme":
        df_edf_abs = pd.read_csv('C:\Users\Admin\Documents\AS 2024 2025\Deuxième semestre\Projet inter-promo\Code\Projet-Interpromo-Groupe-1\data\raw\EDF\bilan-social-d-edf-sa-absenteisme.csv', sep=';')
        #kpi = 
        #df_edf_handi = pd.read_csv('C:\\Users\\Admin\\Documents\\AS 2024 2025\\Deuxième semestre\\Projet inter-promo\\bilan-social-d-edf-sa-salaries-en-situation-de-handicap.csv', sep=';')
        #df_edf_handi = df_edf_handi.drop(['Perimètre juridique', 'Perimètre spatial','Spatial perimeter','Indicator','Type of contract','Employee category','Gender','Unit','Chapitre du bilan social','Unité'], axis=1)
   
### Questions en cours 
# faire une liste de kpi par thématique puis concaténer sur plusieurs thématiques 
# kpi_genre = []
# kpi_conditions_travail = []
# kpi_absentéisme = []
# kpi_age = []
# kpi_handicap = []
# for e in selection:
#   if e.isin(opt_thm) 
# faire liste axes en fonction des possibilités liées au kpi choisi 

df_indicateurs = pd.DataFrame({
    'kpi': ['Salariés en situation de handicap', "Salariés reconnus travailleurs handicapés suite à accidents du travail survenus dans l'entreprise"]}
        )

df_axes_ana = pd.DataFrame({
    'axes': ['Genre','Type de contrat','Collège']}
        )

col1, col2 = st.columns(2)

if selection:  
    with col1:
        opt_id = st.selectbox(
                "Veuillez choisir un indicateur :",
                df_indicateurs,
                index=None,
                placeholder="Sélectionnez un indicateur...",
            )
    if opt_id:
        with col2:
            opt_axe = st.multiselect(
                    "Veuillez choisir un axe d'analyse :",
                    df_axes_ana,
                    placeholder="Sélectionnez un axe d'analyse...",
                )