import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import os 
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container
# Mise en forme avec Streamlit Extras pour ajouter des bordures, etc.
import streamlit_extras 
import chardet

##############################################################
#--########-------DEFINITION DES VARIABLES----######
##############################################################
#---------------Style container-----------------------------
style_container = """{
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    border-radius: 10px;
    background-color: #ffffff;
    }""" 

##############################################################
#--########-------DEFINITION DES FONCTIONS----######
##############################################################
def importation_data (dossier_entreprise, col_inutiles):

    """Fonction qui prends en paramètre le chemin relatif du dossier contenant les données d'une entreprise et les noms de colonnes inutiles
    et retourne la sélection de thémathiques et un dictionnaire (resultats) contenant pour la ou les thématiques choisies:
    - les données associées (entreprise_data) 
    - et la liste de l'ensemble des indicateurs (indicateurs) """

    #----selection Thématique-----------------
    sous_dossiers = [nom for nom in os.listdir(dossier_entreprise) if os.path.isdir(os.path.join(dossier_entreprise, nom))]
    selection = st.pills("Veuillez choisir une ou plusieurs thématiques à étudier :", sous_dossiers, selection_mode='multi')

    #----IMPORTATION DE LA DATA----------------
    if not selection:
        st.write("Veuillez sélectionner au moins une thématique.")
        return ([],{},[])
    else:
        # initialisation dictionnaire pour répertorier les indicateurs et leurs données associées 
        resultats={}
        # parcourir toutes les thématiques sélectionnées 
        for s in selection: 
            file_path=dossier_entreprise+"\\"+s
            noms_fichiers = [f for f in os.listdir(file_path) if f.endswith('.csv')]
            data = []
            # parcourrir tous les fichiers de cette thématique 
            for e in noms_fichiers:
                chemin = os.path.join(file_path,e)
                # Détecter l'encodage du fichier
                with open(chemin, "rb") as f:
                    result = chardet.detect(f.read())
                    encoding_detect = result["encoding"]
                    df = pd.read_csv(chemin, sep=';', encoding='utf-8')
                    data.append(df)
                    df_concatene = pd.concat(data, ignore_index=True)
            # suppression colonnes inutiles 
            for colonne in col_inutiles:
                if colonne in df_concatene.columns:
                    df_concatene = df_concatene.drop(columns=colonne)
            entreprise_data = df_concatene
            indicateurs = sorted(entreprise_data["Indicateur"].astype(str).unique())
            # association liste indicateurs et données associées 
            resultats[s] = {'entreprise_data': entreprise_data, 'indicateurs': indicateurs}
        # lister tous les indicateurs du dictionnaire 
        liste_indicateurs = []
        for selection, contenu in resultats.items(): 
            for indicateur in contenu['indicateurs']: 
                liste_indicateurs.append(indicateur)
        return (selection, resultats, liste_indicateurs)
    
    
def selection_menu (selection, resultats, liste_indicateurs):
    
    """Fonction qui prends en paramètres la sélection de thématiques, le dictionnaire resultats et la liste des indicateurs associés
    et retourne la thématique choisie (selection), l'indicateur choisi (indicateur_), les données en lien (df) et les axes d'analyse (dimension_1 et dimension_2)"""
    
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
        entreprise_data = pd.DataFrame()
        for selection, contenu in resultats.items(): 
            entreprise_data=pd.concat([entreprise_data,contenu['entreprise_data']])
        entreprise_data = entreprise_data.loc[entreprise_data['Indicateur'] == indicateur_]
        df = entreprise_data
        for column in df.columns :
            if df[column].isna().all() :
                df = df.drop(column, axis = 1)
        dimension = df.select_dtypes(include=["object", "category"]).columns.tolist()
        #st.write(df)
        if indicateur_: 
            dimension.remove("Indicateur")
            dimension.remove("Unité")

        #----selection axes d'analyse--------
        if indicateur_:
            st.sidebar.subheader("Axes d'analyse")
            dimension_1 = st.sidebar.selectbox("Veuillez choisir le 1er axe d'analyse :",dimension, index=None, placeholder="Sélectionnez un axe d'analyse...") 
            if dimension_1:
                reste = [d for d in dimension if d != dimension_1]
                for column in reste :
                    if df.loc[df[dimension_1].notna()][column].isna().all() :
                        reste.remove(column)
                dimension_2 = st.sidebar.selectbox("Veuillez choisir le 2eme axe d'analyse :",reste, index=None, placeholder="Sélectionnez un axe d'analyse...")
                return (selection,indicateur_,df,dimension_1,dimension_2)
            else: 
                return (selection,indicateur_,df,None,None)
        else:
            st.write("Veuillez saisir un indicateur.")
            return (selection,None,[],None,None)
        
            
def titre (variable):

    """Fonction qui prend en paramètre la variable du titre
    et retourne l'affichage."""

    st.markdown(f"""<div style='text-align: center; 
                font_size: 20px;
                font-weight: bold;'> Evolution de l'indicateur 
                <i>{variable.lower()}</i> par année </div>""",
                unsafe_allow_html=True)
    

def mise_en_forme_graph (nom_fig, key_fig, indicateur_, df):

    """Fonction qui prend en paramètre le nom de la figure, son indentfiant, l'indicateur et ses données en lien  
    et retourne la mise en forme permattant l'affichage du graphique."""

    with stylable_container(key=key_fig,
                            css_styles=style_container): 
            st.plotly_chart(
                    nom_fig.update_layout(
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),  # Légende en haut
                        margin=dict(l=10, r=10, t=0, b=10),  # Marges pour éviter que ça soit trop collé
                        height=300,  # Taille réduite du graphique pour qu'il rentre bien
                        yaxis_title="Valeur en "+df["Unité"].iloc[0]
                    ),
                    use_container_width=True
                )
    titre(indicateur_)


def titre_une_annee(variable,annee):

    """Fonction qui prend en paramètre la variable du titre et l'année et retourne l'affichage."""

    st.markdown(f"""<div style='text-align: center; 
                font_size: 20px;
                font-weight: bold;'> Evolution de l'indicateur 
                <i>{variable.lower()}</i> pour l'année {annee}</div>""",
                unsafe_allow_html=True)


def affichage_une_annee (indicateur_, df, dimension_1, dimension_2):

    """Fonction qui prends en paramètre l'indicateur (indicateur_) et son jeu de données (df) et les listes des dimensions possibles (dimension_1 et dimension_2)
    et retourne l'affichage du graphique pour une dimension et une année."""

    annees = df["Année"].unique().tolist()
    annee = st.selectbox("Veuillez choisir une année :",annees, index=None, placeholder="Sélectionnez une année...")
    if annee:
        df = df[df["Année"] == annee]
        df_grouped = df.groupby([dimension_1,dimension_2], as_index=False).sum()
        fig_bar=px.bar(df_grouped, x=dimension_2,
                    y="Valeur",
                    color=dimension_1,
                    barmode="group",
                    labels={dimension_1},
                    color_discrete_sequence=px.colors.qualitative.D3)
        st.plotly_chart(fig_bar.update_layout(yaxis_title="Valeur en "+df["Unité"].iloc[0]))
        titre_une_annee(indicateur_, annee)


def affichage_graphs (selection, indicateur_, df, dimension_1, dimension_2):

    """Fonction qui prends en paramètres la ou les thématiques, l'indicateur choisi, les données en lien et les axes d'analyse choisis
    et qui retourne l'affichage de l'ensembles des graphiques."""

    #----------------Graph simple évol au cours du temps---------
    if selection and indicateur_ and not dimension_1:
        df_grouped = df.groupby(["Année"], as_index=False).sum()

        fig_ligne=px.line(df_grouped, x="Année",
                        y="Valeur", 
                        markers=True,
                        color_discrete_sequence=px.colors.qualitative.D3
                        )
        fig_bar=px.bar(df_grouped, x="Année",
                y="Valeur",
                color=dimension_1,
                color_discrete_sequence=px.colors.qualitative.D3 )

        a,b=st.columns(2)
        with a:
            mise_en_forme_graph (fig_bar, "graph_containera", indicateur_, df)
        with b:
            mise_en_forme_graph (fig_ligne, "graph_containerb", indicateur_, df)

    #----------------Graph univarié-----------------------------
    elif selection and indicateur_ and dimension_1 and not dimension_2:
        df_grouped = df.groupby(["Année",dimension_1], as_index=False).sum()

        fig_ligne=px.line(df_grouped, x="Année",
                        y="Valeur", 
                        color=dimension_1,
                        labels={dimension_1, "Valeur: "+indicateur_},
                        markers=True,
                        color_discrete_sequence=px.colors.qualitative.D3
                        )
        fig_bar=px.bar(df_grouped, x="Année",
                y="Valeur",
                color=dimension_1,
                barmode="group",
                labels={dimension_1, "Valeur: "+indicateur_},
                color_discrete_sequence=px.colors.qualitative.D3 )

        a,b=st.columns(2)
        with a:
            mise_en_forme_graph (fig_bar, "graph_containera", indicateur_, df)
        with b:
            mise_en_forme_graph (fig_ligne, "graph_containerb", indicateur_, df)

    elif selection and indicateur_ and dimension_1:
    #----------------Graph multiple----------------------------

        df_grouped = df.groupby(["Année",dimension_1,dimension_2], as_index=False).sum()
        fig_secteur = px.sunburst(df_grouped, path=["Année",dimension_1,dimension_2], values="Valeur")
        fig_multi_lignes = px.line(df_grouped, x="Année", y="Valeur", 
                                    color=dimension_1, line_dash=dimension_2,
                                    markers=True)

        col1, col2 = st.columns(2)

        # Colonne 1 : Secteur 
        with col1:
            mise_en_forme_graph (fig_secteur, "graph_container1", indicateur_, df)

        # Colonne 2 : Multi-lignes
        with col2:
            mise_en_forme_graph (fig_multi_lignes, "graph_container2", indicateur_, df)

        st.write(" ")
        st.write(" ")
        filtre = st.checkbox("Afficher le graphique sur une seule année.")
        if filtre:
            return(affichage_une_annee(indicateur_,df,dimension_1, dimension_2))
