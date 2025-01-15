import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.title("Visualusation des indicateur" )

st.markdown("Nous allons afficher les graphiques:")


##         Salariés en situation de hadicap 
st.title("Salariés en situation de hadicap" )

df = pd.read_csv("D:/Mon M1/EDF/Projet-Interpromo-Groupe-1/data/transformed/EDF/handicap/sal_handicap.csv", sep=";")
st.write(df.head(10))
#Figure  
fig = px.bar(data_frame = df, x="Année", y = "Valeur", title="Nombre de Salariés en situation de hadicap par Année")
st.plotly_chart(fig)

 # Grouper les données par Année_Genre et calculer le total
st.header("1 : Nombre de Salariés en situation de hadicap par Année et Genre")
total_par_année_genre = df.groupby(['Année', 'Genre'])['Valeur'].sum().reset_index()
st.write("Nombre de salariés en situation de handicap par année_Genre:")
st.write(total_par_année_genre)
# figure
fig = px.bar(
    total_par_année_genre,
    x='Année',
    y='Valeur',
    color='Genre',
    barmode='group',  # Barres groupées par genre
    title="Graphe: Nombre de salariés en situation de handicap par année et par genre",
    labels={'nombre_de_salariés_handicap': 'Nombre de salariés'}
)
st.plotly_chart(fig)

# Représentation de l'évolution du nombre de salariés par genre avec des lignes
fig = px.line(
    total_par_année_genre,
    x='Année',
    y='Valeur',
    color='Genre',
    markers=True,
    title="Évolution du nombre de salariés en situation de handicap par année et par genre",
    labels={"Valeur": 'nombre_de_salariés_handicap'},
)
st.plotly_chart(fig)


##         Salariés reconnus travailleurs handicapés suite à accidents du travail survenus dans l'entreprise 
# Ici il n'y avait pas de genre dans la dataframe
st.header("2 : Nombre de salariés reconnus travailleurs handicapés suite à accidents du travail survenus dans l'entreprise par Année")
df = pd.read_csv("D:/Mon M1/EDF/Projet-Interpromo-Groupe-1/data/transformed/EDF/handicap/sal_handicap_at.csv", sep=";")
total_par_année = df.groupby(['Année'])['Valeur'].sum().reset_index()
st.write("Nombre de salariés reconnus travailleurs handicapés suite à accidents du travail survenus dans l'entreprise:")
st.write(total_par_année)
#Figure 
 
fig = px.bar(data_frame = df, x="Année", y = "Valeur", title="Graphe: Nombre de Salariés reconnus travailleurs handicapés suite à accidents du travail survenus dans l'entreprise")
st.plotly_chart(fig)

# Représentation de  l'évolution du nombre de salariés reconnus travailleurs handicapés suite à accidents du travail survenus dans l'entreprise par année avec des lignes
fig = px.line(
    total_par_année,
    x='Année',
    y='Valeur',
    markers=True,
    title="Évolution du nombre de salariés reconnus travailleurs handicapés suite à accidents du travail survenus dans l'entreprise par année",
    labels={"Valeur": 'nombre_de_salariés_handicap'},
)
st.plotly_chart(fig)


##           Nbre de stagiairres scolaire par Année

df = pd.read_csv("D:/Mon M1/EDF/Projet-Interpromo-Groupe-1/data/transformed/EDF/exterieur/stagiaires_scolaires.csv", sep=";")
st.header("3 : Nombre de stagiairres scolaire par Année par Année et Genre")
total_par_année_genre = df.groupby(['Année', 'Genre'])['Valeur'].sum().reset_index()
st.write("Nombre de stagiairres scolaire par année_Genre:")
st.write(total_par_année_genre)
#Figure  
fig = px.bar(
    total_par_année_genre,
    x='Année',
    y='Valeur',
    color='Genre',
    barmode='group',  # Barres groupées par genre
    title="Graphe: Nombre de stagiairres scolaire par année et par genre",
    labels={"Valeur": 'Nombre de stagiairres scolaire'}
)
# Afficher le graphique
st.plotly_chart(fig)

# Représentation de l'évolution du Nombre de stagiairres scolaire par Année_genre avec des lignes
fig = px.line(
    total_par_année_genre,
    x='Année',
    y='Valeur',
    color='Genre',
    markers=True,
    title="Évolution du Nombre de stagiairres scolaire par année et par genre",
    labels={"Valeur": 'Nombre de stagiairres scolaire'},
)
st.plotly_chart(fig)



##  nbre de Salarié exterieur par année 

#       Salariés détachés accueillis
df = pd.read_csv("D:/Mon M1/EDF/Projet-Interpromo-Groupe-1/data/transformed/EDF/exterieur/sal_detaches_accueillis.csv", sep=";")
st.header("4 : Nombre de Salariés détachés accueillis par Année et Genre")
total_par_année_genre = df.groupby(['Année', 'Genre'])['Valeur'].sum().reset_index()
st.write("Nombre de Salariés détachés accueillis par année_Genre:")
st.write(total_par_année_genre)
#Figure  
fig = px.bar(
    total_par_année_genre,
    x='Année',
    y='Valeur',
    color='Genre',
    barmode='group',  # Barres groupées par genre
    title="Graphe: Nombre de Salariés détachés accueillis par année et par genre",
    labels={'Nombre de Salariés détachés accueillis'}
)
# Afficher le graphique
st.plotly_chart(fig)

# Représentation de l'évolution du Nombre de Salariés détachés accueillis par Année_genre avec des lignes
fig = px.line(
    total_par_année_genre,
    x='Année',
    y='Valeur',
    color='Genre',
    markers=True,
    title="Évolution du Nombre de Salariés détachés accueillis par année et par genre",
    labels={"Valeur": 'Nombre de Salariés détachés accueillis'},
)
st.plotly_chart(fig)


#    Nombre moyen mensuel de travailleurs temporaires
df = pd.read_csv("D:/Mon M1/EDF/Projet-Interpromo-Groupe-1/data/transformed/EDF/exterieur/nb_moyen_temp.csv", sep=";")
st.header("5 : nombre moyen mensuel de travailleurs temporaires par Année et Genre")
total_par_année_genre = df.groupby(['Année', 'Genre'])['Valeur'].sum().reset_index()
st.write("Nombre moyen mensuel de travailleurs temporaires par année_Genre:")
st.write(total_par_année_genre)
#Figure  
fig = px.bar(
    total_par_année_genre,
    x='Année',
    y='Valeur',
    color='Genre',
    barmode='group',  # Barres groupées par genre
    title="Graphe: Nombre moyen mensuel de travailleurs temporaires par année et genre",
    labels={'Nombre moyen mensuel de travailleurs temporaires'}
)
st.plotly_chart(fig)

# Représentation de l'évolution du Nombre moyen mensuel de travailleurs temporaires par Année_genre avec des lignes
fig = px.line(
    total_par_année_genre,
    x='Année',
    y='Valeur',
    color='Genre',
    markers=True,
    title="Évolution du Nombre moyen mensuel de travailleurs temporaires par année et genre",
    labels={"Valeur": 'Nombre moyen mensuel de travailleurs temporaires'},
)
st.plotly_chart(fig)


#    Embauches de salariés de moins de 25 ans par Annnée
df = pd.read_csv("D:/Mon M1/EDF/Projet-Interpromo-Groupe-1/data/transformed/EDF/effectif/embauches_moins25.csv", sep=";")
st.header("5 : Nombre Embauches de salariés de moins de 25 ans par Année par Année et Genre")
total_par_année_genre = df.groupby(['Année', 'Genre'])['Valeur'].sum().reset_index()
st.write("Nombre Embauches de salariés de moins de 25 ans par année_Genre:")
st.write(total_par_année_genre)
#Figure  
fig = px.bar(
    total_par_année_genre,
    x='Année',
    y='Valeur',
    color='Genre',
    barmode='group',  # Barres groupées par genre
    title="Graphe: Nombre Embauches de salariés de moins de 25 ans par année_Genre",
    labels={'Nombre Embauches de salariés de moins de 25 ans par année_Genre'}
)
st.plotly_chart(fig)

# Représentation de l'évolution du Nombre Embauches de salariés de moins de 25 ans par Année_genre avec des lignes
fig = px.line(
    total_par_année_genre,
    x='Année',
    y='Valeur',
    color='Genre',
    markers=True,
    title="Évolution du Nombre Embauches de salariés de moins de 25 ans par année et genre",
    labels={"Valeur": 'Nombre Embauches de salariés de moins de 25 ans'},
)
st.plotly_chart(fig)


#     Nombre demissions par Annnée
df = pd.read_csv("D:/Mon M1/EDF/Projet-Interpromo-Groupe-1/data/transformed/EDF/effectif/demissions.csv", sep=";")
st.header("6 : Nombre demissions par Année et Genre")
total_par_année_genre = df.groupby(['Année', 'Genre'])['Valeur'].sum().reset_index()
st.write("Nombre demissions par année_Genre:")
st.write(total_par_année_genre)
#Figure  
fig = px.bar(
    total_par_année_genre,
    x='Année',
    y='Valeur',
    color='Genre',
    barmode='group',  # Barres groupées par genre
    title="Graphe: Nombre demissions par année_Genre",
    labels={"Valeur": "Nombre demissions par année_Genre"}
)
# Afficher le graphique
st.plotly_chart(fig)

# Représentation de l'évolution du Nombre demissions par Année_genre avec des lignes
fig = px.line(
    total_par_année_genre,
    x='Année',
    y='Valeur',
    color='Genre',
    markers=True,
    title="Évolution du Nombre demissions par année et genre",
    labels={"Valeur": 'Nombre demissions par année_Genre'},
)
st.plotly_chart(fig)



#    Absence pour maladie
df = pd.read_csv("D:/Mon M1/EDF/Projet-Interpromo-Groupe-1/data/transformed/EDF/absenteisme/abs_maladie.csv", sep=";")
st.header("7 : Nombre Absence pour maladie par Année et Genre")
total_par_année_genre = df.groupby(['Année', 'Genre'])['Valeur'].sum().reset_index()
st.write("Nombre Absence pour maladie par année_Genre:")
st.write(total_par_année_genre)
#Figure  
fig = px.bar(
    total_par_année_genre,
    x='Année',
    y='Valeur',
    color='Genre',
    barmode='group',  # Barres groupées par genre
    title="Graphe: Nombre Absence pour maladie par année_Genre",
    labels={'Valeur':'Nombre Absence pour maladie'}
)
st.plotly_chart(fig)

# Représentation de l'évolution du Nombre Absence pour maladie par Année_genre avec des lignes
fig = px.line(
    total_par_année_genre,
    x='Année',
    y='Valeur',
    color='Genre',
    markers=True,
    title="Évolution du Nombre Absence pour maladie par année et genre",
    labels={"Valeur": 'Nombre Absence pour maladie'},
)
st.plotly_chart(fig)


#  Absence pour congé de maternité ou d'adoption
# ici pas besoins du Genre 
df = pd.read_csv("D:/Mon M1/EDF/Projet-Interpromo-Groupe-1/data/transformed/EDF/absenteisme/abs_mat_adoption.csv", sep=";")
st.header("8 : Nombre Absence pour congé de maternité ou d'adoption par Année")
total_par_année = df.groupby(['Année'])['Valeur'].sum().reset_index()
st.write("Nombre Absence pour congé de maternité ou d'adoption par année:")
st.write(total_par_année)
#Figure  
fig = px.bar(data_frame = df, x="Année", y = "Valeur", title="Graphe: Nombre Absence pour congé de maternité ou d'adoption par année")
st.plotly_chart(fig)

# Représentation de l'évolution du Nombre Absence pour congé de maternité ou d'adoption par Année avec des lignes
fig = px.line(
    total_par_année,
    x='Année',
    y='Valeur',
    markers=True,
    title="Évolution du Nombre Absence pour congé de maternité ou d'adoption par année",
    labels={"Valeur": "Nombre Absence pour congé de maternité ou d'adoption"},
)
st.plotly_chart(fig)



#     Absence pour congé de paternité et d'accueil de l'enfant
# ici pas besoins du Genre
df = pd.read_csv("D:/Mon M1/EDF/Projet-Interpromo-Groupe-1/data/transformed/EDF/absenteisme/abs_paternite.csv", sep=";")
st.header("9 : Nombre Absence pour congé de paternité et d'accueil de l'enfant par Année")
total_par_année = df.groupby(['Année'])['Valeur'].sum().reset_index()
st.write("Nombre Absence pour congé de paternité et d'accueil de l'enfant par année:")
st.write(total_par_année)
#Figure  
fig = px.bar(data_frame = df, x="Année", y = "Valeur", title="Graphe: Nombre Absence pour congé de paternité et d'accueil de l'enfant par année")
st.plotly_chart(fig)

# Représentation de l'évolution du Nombre Absence pour congé de paternité et d'accueil de l'enfant par Année avec des lignes
fig = px.line(
    total_par_année,
    x='Année',
    y='Valeur',
    markers=True,
    title="Évolution du Nombre Absence pour congé de paternité et d'accueil de l'enfant par année",
    labels={"Valeur": "Nombre Absence pour congé de paternité et d'accueil de l'enfant"},
)
st.plotly_chart(fig)




# salariés ayant bénéficié d’un congé individuel de formation non rémunéré
df = pd.read_csv("D:/Mon M1/EDF/Projet-Interpromo-Groupe-1/data/transformed/EDF/formation/cif_non_remun.csv", sep=";")
st.header("10 : Nombre de salariés ayant bénéficié d’un congé individuel de formation non rémunéré par Année et Genre")
total_par_année_genre = df.groupby(['Année', 'Genre'])['Valeur'].sum().reset_index()
st.write("Nombre de salariés ayant bénéficié d’un congé individuel de formation non rémunéré par année_Genre:")
st.write(total_par_année_genre)
#Figure  
fig = px.bar(
    total_par_année_genre,
    x='Année',
    y='Valeur',
    color='Genre',
    barmode='group',  # Barres groupées par genre
    title="Graphe: Nombre de salariés ayant bénéficié d’un congé individuel de formation non rémunéré par année_Genre",
    labels={'Valeur': 'Salariés ayant bénéficié_congé_formation non rémunéré', 'Année': 'année', 'Genre': 'genre'}
)
st.plotly_chart(fig)

# Représentation de l'évolution du Nombre de Salariés ayant bénéficié_congé_formation non rémunéré par Année_genre avec des lignes
fig = px.line(
    total_par_année_genre,
    x='Année',
    y='Valeur',
    color='Genre',
    markers=True,
    title="Évolution du Nombre de Salariés ayant bénéficié_congé_formation non rémunéré par année et genre",
    labels={"Valeur": 'Salariés ayant bénéficié_congé_formation non rémunéré'},
)
st.plotly_chart(fig)