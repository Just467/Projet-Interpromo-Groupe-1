import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import os 
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container
# Mise en forme avec Streamlit Extras pour ajouter des bordures, etc.
import streamlit_extras 

st.set_page_config(layout="wide")  # Utiliser toute la largeur de l'écran

### Définition de la fonction ###

def selection_menu (dossier_entreprise, col_inutiles):

    """Fonction qui prendre en paramètre le chemin relatif du dossier contenant les données d'une entreprise et les noms de colonnes inutiles
    et retourne la thématique choisie (selection), l'indicateur choisi (indicateur_), les données en lien (df) et les axes d'analyse (dimension_1 et dimension_2)"""

    #----selection Thématique-----------------
    sous_dossiers = [nom for nom in os.listdir(dossier_entreprise) if os.path.isdir(os.path.join(dossier_entreprise, nom))]
    selection = st.pills("Veuillez choisir une ou plusieurs thématiques à étudier :", sous_dossiers, selection_mode="multi")

    #----IMPORTATION DE LA DATA----------------
    if not selection:
        st.write("Veuilliez sélectionner au moins une thématique.")
        return ([],None,[],None,None)
    else:
        # initialisation dictionnaire pour répertorier les indicateurs et leurs données associées 
        resultats={}
        # parcourir toutes les thématiques sélectionnées 
        for s in selection: 
            file_path="..\\data\\transformed\\EDF\\"+s
            noms_fichiers = [f for f in os.listdir(file_path) if f.endswith('.csv')]
            data = []
            # parcourrir tous les fichiers de cette thématique 
            for e in noms_fichiers:
                chemin = os.path.join(file_path,e)
                df = pd.read_csv(chemin, sep=';')
                data.append(df)
            df_concatene = pd.concat(data, ignore_index=True)
            # suppression colonnes inutiles 
            for colonne in col_inutiles:
                if colonne in df_concatene.columns:
                    df_concatene = df_concatene.drop(columns=colonne)
            entreprise_data = df_concatene
            indicateurs = sorted(entreprise_data["Indicateur"].unique())
            # association liste indicateurs et données associées 
            resultats[s] = {'entreprise_data': entreprise_data, 'indicateurs': indicateurs}
        # lister tous les indicateurs du dictionnaire 
        liste_indicateurs = []
        for dossier, contenu in resultats.items(): 
            for indicateur in contenu['indicateurs']: 
                liste_indicateurs.append(indicateur)

        #----selection d'indicateurs--------
        if selection:  
            st.sidebar.subheader("Indicateur")
            indicateur_ = st.sidebar.selectbox(
                    "Veuillez choisir un indicateur :",
                    liste_indicateurs,
                    index=None,
                    placeholder="Sélectionnez un indicateur...",
                )
            # récupération données liées à l'indicateur choisi 
            for dossier, contenu in resultats.items(): 
                for indicateur in contenu['indicateurs']: 
                    if indicateur == indicateur_:
                        entreprise_data=contenu['entreprise_data']
            df = entreprise_data[entreprise_data["Indicateur"] == indicateur_]
            dimension = df.select_dtypes(include=["object", "category"]).columns.tolist()
            dimension.remove("Indicateur")

            #----selection axes d'analyse--------
            if indicateur_:
                st.sidebar.subheader("Axes d'analyse")
                dimension_1 = st.sidebar.selectbox("Veuillez choisir le 1er axe d'analyse :",dimension, index=None, placeholder="Sélectionnez un axe d'analyse...") 
                if dimension_1:
                    reste = [d for d in dimension if d != dimension_1]
                    dimension_2 = st.sidebar.selectbox("Veuillez choisir le 2eme axe d'analyse :",reste, index=None, placeholder="Sélectionnez un axe d'analyse...")
                    return (selection,indicateur_,df,dimension_1,dimension_2)
                else: 
                    st.write("Veuillez sélectionner au moins un axe d'analyse.")
                    return (selection,indicateur_,df,None,None)
            else:
                return (selection,None,df,None,None)

### Appel de la fonction ###

dossier_entreprise = "E:/perso/Année scolaire 2024-2025/Cours/PIP/Projet-Interpromo-Groupe-1/data/transformed/EDF"
col_inutiles = ["Perimètre juridique","Perimètre spatial","Chapitre du bilan social","Unité","Plage M3E"]
selection, indicateur_, df, dimension_1, dimension_2 = selection_menu(dossier_entreprise,col_inutiles)

##############################################################
#--########-------CREATION DES GRAPHIQUES----######
##############################################################

#---------------Style container-----------------------------
style_container = """{
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    border-radius: 10px;
    background-color: #ffffff;
    }""" 

#----------------Graph univarié-----------------------------
if not dimension_2:
    df_grouped = df.groupby(["Année",dimension_1], as_index=False).sum()

    fig_ligne=px.line(df_grouped, x="Année",
                    y="Valeur",
                    color=dimension_1,
                    labels={dimension_1, "Valeur: "+indicateur_},
                    # title="Evolution des "+ indicateur_+ "des employés par année",
                    color_discrete_sequence=px.colors.qualitative.D3
                    )
    fig_bar=px.bar(df_grouped, x="Année",
            y="Valeur",
            color=dimension_1,
            barmode="group",
            labels={dimension_1, "Valeur: "+indicateur_},
        #     title="Evolution des "+ indicateur_+ "des employés par année",
            color_discrete_sequence=px.colors.qualitative.D3 )

    a,b=st.columns(2)
    with a:
        st.plotly_chart(fig_bar)
    with b:
        st.plotly_chart(fig_ligne)
else:
#----------------Graph multiple----------------------------

    df_grouped = df.groupby(["Année",dimension_1,dimension_2], as_index=False).sum()
    fig_secteur = px.sunburst(df_grouped, path=["Année",dimension_1,dimension_2], values="Valeur")
                    # title=indicateur_+ " des employés par année"
    fig_multi_lignes = px.line(df_grouped, x="Année", y="Valeur", 
                                   color=dimension_1, line_dash=dimension_2)

    col1, col2 = st.columns(2)

    # Colonne 1 : Secteur 
    with col1:
        with stylable_container(key="graph_container1",
                            css_styles=style_container): 
            
            st.plotly_chart(
                    fig_secteur.update_layout(
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),  # Légende en haut
                        margin=dict(l=10, r=10, t=0, b=10),  # Marges pour éviter que ça soit trop collé
                        height=300  # Taille réduite du graphique pour qu'il rentre bien
                    ),
                    use_container_width=True
                )

    # Colonne 2 : Multi-lignes
    with col2:
        with stylable_container(key="graph_container2",
                            css_styles=style_container):
            # Titre et graphique Carte
            #st.markdown("<h3 style='text-align: center; font-size: 16px;'>Carte</h3>", unsafe_allow_html=True)
            st.plotly_chart(
                fig_multi_lignes.update_layout(
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),  # Légende en haut
                    margin=dict(l=10, r=10, t=0, b=10),  # Marges pour éviter que ça soit trop collé
                    height=300  # Taille réduite du graphique pour qu'il rentre bien
                ),
                use_container_width=True
            )








