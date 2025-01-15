
# Importation des bibliothèques 
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px 

st.write('# Dashboard')

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

if option == 'Genre' and entreprise == "Decathelon":
    # Données genre Decathelon monde 2022
    dfg = pd.DataFrame({
        'sizes': [46.3, 53.7],
        'labels': ['Femmes', 'Hommes']}
        )
    # Créer un diagramme circulaire
    graph = px.pie(dfg, values='sizes', names='labels', title='Effectif par genre chez Decathelon dans le monde en 2022')
    # Afficher le tracé dans Streamlit
    st.plotly_chart(graph)

    # Proportion de femmes et d'hommes pour 2022 et 2023 par périmétre monde (Monde  / Europe / Asie / Afrique et Moyen-Orient / Amériques / Océanie)
    # Pour affichage si case cochée 
    if st.checkbox('Montrer répartition par zone géographique'):
        df2022 = pd.DataFrame({
            'femmes': [47.2, 45, 42.4, 43.4,38.6],
            'hommes': [52.8, 55, 57.6,56.6,61.4],
            'Zone géographique': ['Europe 2022','Asie 2022','Afrique et Moyen-Orient 2022','Amériques 2022','Océanie 2022']}
            )
        df2023 = pd.DataFrame({
            'femmes': [46.8, 44.9, 43.8, 44.7,39.3],
            'hommes': [53.2, 55.1, 56.2,55.3,60.7],
            'Zone géographique': ['Europe 2023','Asie 2023','Afrique et Moyen-Orient 2023','Amériques 2023','Océanie 2023']}
            )
        # Jointure pour avoir les deux années dans un même data frame 
        dftot = pd.concat([df2022, df2023], ignore_index=True)
        # Tri par ordre alphabétique pour avoir les deux années par zone géographique 
        dftot_trie = dftot.sort_values(by='Zone géographique')
        # conversion data frame pour affichage 
        dftot_long = pd.melt(dftot_trie, id_vars=['Zone géographique'], value_vars=['femmes', 'hommes'], var_name='Genre', value_name='Proportion')
        # création d'un diagramme en barres 
        fig = px.bar(dftot_long, y='Zone géographique', x='Proportion', color='Genre', barmode='stack', title='Proportions par Zone Géographique et Année')
        # Ajout ligne verticale à 50 % pour visualisation parité 
        fig.add_vline(x=50, line_width=3, line_dash="dash", line_color="red")
        # Affichage 
        st.plotly_chart(fig)

elif option == 'Age' and entreprise == "Decathelon":
    # Données tranches d'age Decathelon monde 2022 et 2023 
    dfage = pd.DataFrame({
        '2022': [56.8, 5.1, 51.7, 39.4, 29.8, 9.6, 3.8],
        '2023': [54.5, 5.1, 49.4, 41.1, 30.7, 10.4, 4.4]},
        index = ['moins de 29 ans','moins de 20 ans','de 20 ans à 29 ans','entre 30 et 49 ans','de 30 ans à 39 ans', 'de 40 ans à 49 ans', '50 ans et plus']
        )
    # Création diagramme 
    graph_age = px.bar(dfage,barmode='group', title="Effectif par tranche d'age et par année dans le monde")
    graph_age.update_layout(xaxis_title=None, yaxis_title='Proportion', legend_title='Année')
    # Affichage 
    st.plotly_chart(graph_age)

if option == 'Handicap' and entreprise == "EDF":
    # Données de EDF sur le handicap en France 
    df_edf_handi = pd.read_csv('C:\\Users\\Admin\\Documents\\AS 2024 2025\\Deuxième semestre\\Projet inter-promo\\bilan-social-d-edf-sa-salaries-en-situation-de-handicap.csv', sep=';')
    df_edf_handi = df_edf_handi.drop(['Perimètre juridique', 'Perimètre spatial','Spatial perimeter','Indicator','Type of contract','Employee category','Gender','Unit','Chapitre du bilan social','Unité'], axis=1)
    indicateur = st.selectbox(
        "Veuillez choisir un indicateur",
        ("Salariés reconnus travailleurs handicapés suite à accidents du travail survenus dans l'entreprise", "Salariés en situation de handicap", "Evolution du nombre de salariés en situation de handicap au cours du temps"),
        index=None,
        placeholder="Sélectionnez un indicateur...",
    )
    filtre = [indicateur] 
    if indicateur == "Salariés reconnus travailleurs handicapés suite à accidents du travail survenus dans l'entreprise":
        df_edf_handi_accident = df_edf_handi[df_edf_handi['Indicateur'].isin(filtre)]
        affichage_accident = px.bar(df_edf_handi_accident, y='Type de contrat', x='Valeur', color='Collège', barmode='stack', title="Effectif travailleurs handicapés post accident du travail par type de contrat et de collège de 2017 à 2023")
        affichage_accident.update_layout(xaxis_title='Effectif')
        st.plotly_chart(affichage_accident)
    elif indicateur == "Salariés en situation de handicap":
        df_edf_situ_handi = df_edf_handi[df_edf_handi['Indicateur'].isin(filtre)]
        affichage_situ_handi = px.sunburst(df_edf_situ_handi, path=['Collège','Type de contrat'], values='Valeur', title="Effectif de salariés en situation de handicap par type de contrat et de collège de 2017 à 2023")
        st.plotly_chart(affichage_situ_handi)
        if st.checkbox('Montrer répartition par genre'):
            affichage_situ_handi_genre = px.sunburst(df_edf_situ_handi, path=['Collège','Type de contrat','Genre'], values='Valeur')
            st.plotly_chart(affichage_situ_handi_genre)
    elif indicateur == "Evolution du nombre de salariés en situation de handicap au cours du temps":
        df_tot = df_edf_handi.groupby(['Année','Collège','Genre'])['Valeur'].sum().reset_index()
        affichage_evol_temps = px.line(df_tot, x="Année", y="Valeur", color='Collège', line_dash='Genre', title='Evolution du nombre de salariés en situation de handicap au cours du temps par collège')
        st.plotly_chart(affichage_evol_temps)

    
    

