import streamlit as st
from utils import  selection_menu, affichage_graphs
import os
import pandas as pd
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.switch_page_button import switch_page

def importation_data(dossier_entreprise, col_inutiles):
    """
    Fonction qui explore tous les sous-dossiers d'un dossier donné pour collecter les fichiers CSV,
    et extrait les indicateurs à partir des fichiers CSV. Les colonnes inutiles sont supprimées si présentes.

    Arguments :
        dossier_entreprise : str - Chemin relatif vers le dossier contenant les données.
        col_inutiles : list - Liste des colonnes à supprimer.

    Retourne :
        - Un dictionnaire contenant pour chaque sous-dossier :
            - Les données concaténées (`entreprise_data`)
            - La liste des indicateurs (`indicateurs`)
        - Une liste consolidée des indicateurs de tous les sous-dossiers.
    """
    # Initialisation du dictionnaire pour stocker les données et indicateurs
    resultats = {}
    liste_indicateurs = set()

    # Parcourir tous les sous-dossiers
    sous_dossiers = [nom for nom in os.listdir(dossier_entreprise) if os.path.isdir(os.path.join(dossier_entreprise, nom))]

    for sous_dossier in sous_dossiers:
        file_path = os.path.join(dossier_entreprise, sous_dossier)
        noms_fichiers = [f for f in os.listdir(file_path) if f.endswith('.csv')]

        if not noms_fichiers:
            st.warning(f"Aucun fichier trouvé dans le dossier : {file_path}")
            continue

        data = []
        for fichier in noms_fichiers:
            chemin = os.path.join(file_path, fichier)
            try:
                df = pd.read_csv(chemin, sep=';')
                data.append(df)
            except Exception as e:
                st.error(f"Erreur lors de la lecture du fichier {fichier} : {e}")
                continue

        # Concaténer les données de tous les fichiers dans le sous-dossier
        df_concatene = pd.concat(data, ignore_index=True)

        # Suppression des colonnes inutiles
        df_concatene = df_concatene.drop(columns=col_inutiles, errors='ignore')

        # Extraire les indicateurs
        if "Indicateur" in df_concatene.columns:
            indicateurs = sorted(df_concatene["Indicateur"].unique())
        else:
            st.warning(f"Colonne 'Indicateur' non trouvée dans les fichiers de {sous_dossier}.")
            indicateurs = []

        # Ajouter les indicateurs au set global
        liste_indicateurs.update(indicateurs)

        # Stocker les résultats pour ce sous-dossier
        resultats[sous_dossier] = {
            'entreprise_data': df_concatene,
            'indicateurs': indicateurs
        }

    # Retourner le dictionnaire des résultats et la liste globale des indicateurs
    return resultats, sorted(liste_indicateurs)

import os
import pandas as pd
import streamlit as st

def extraire_indicateur(dossier_entreprise, indicateur_recherche):
    """
    Fonction qui explore tous les sous-dossiers d'un dossier donné, charge les fichiers CSV,
    et renvoie une DataFrame contenant uniquement les lignes correspondant à un indicateur spécifique.

    Arguments :
        dossier_entreprise : str - Chemin relatif vers le dossier contenant les données.
        indicateur_recherche : str - L'indicateur que l'on souhaite extraire.

    Retourne :
        - DataFrame contenant les lignes de données correspondant à l'indicateur spécifié.
        - Si l'indicateur n'est pas trouvé, un message d'avertissement est affiché.
    """
    # Initialiser une liste pour stocker les données filtrées
    donnees_filtrees = []

    # Parcourir tous les sous-dossiers
    try:
        sous_dossiers = [nom for nom in os.listdir(dossier_entreprise) if os.path.isdir(os.path.join(dossier_entreprise, nom))]
    except FileNotFoundError as e:
        st.error(f"Erreur d'accès au dossier : {e}")
        return pd.DataFrame()  # Retourne une DataFrame vide en cas d'erreur

    for sous_dossier in sous_dossiers:
        file_path = os.path.join(dossier_entreprise, sous_dossier)
        noms_fichiers = [f for f in os.listdir(file_path) if f.endswith('.csv')]

        if not noms_fichiers:
            st.warning(f"Aucun fichier CSV trouvé dans le dossier : {file_path}")
            continue

        for fichier in noms_fichiers:
            chemin = os.path.join(file_path, fichier)
            try:
                df = pd.read_csv(chemin, sep=';')
                
                # Filtrer les données par l'indicateur recherché
                df_filtre = df[df['Indicateur'] == indicateur_recherche]

                if not df_filtre.empty:
                    donnees_filtrees.append(df_filtre)
            except pd.errors.ParserError as e:
                st.error(f"Erreur de lecture du fichier {fichier} : {e}")
                continue
            except Exception as e:
                st.error(f"Erreur inconnue lors de la lecture du fichier {fichier} : {e}")
                continue

    # Si des données ont été trouvées pour l'indicateur, les concaténer et les retourner
    if donnees_filtrees:
        df_resultat = pd.concat(donnees_filtrees, ignore_index=True)
        return df_resultat
    else:
        st.warning(f"Aucune donnée trouvée pour l'indicateur '{indicateur_recherche}' dans les fichiers.")
        return pd.DataFrame()  # Retourne une DataFrame vide si aucune donnée n'a été trouvée

button_style = """button{
    opacity: 0;
    padding-top: 100%;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 1;
    margin: 0;
    float: none;
}
"""
container_style = """{
    z-index: 0;
    background_color: #171717;
    border-top: 2px solid #373737;
}
"""
col_inutiles = ["Perimètre juridique","Perimètre spatial","Chapitre du bilan social","Unité","Plage M3E"]

st.title("Comparaison des indicateurs")
entreprises = ["EDF", "INSA", "CNP", "DECATHLON","ENGIE"]
selected_entreprises = st.multiselect(
    "Veuillez 2 entreprises: ",
    entreprises,
    default = None,
    max_selections = 2
    )

entreprise_1 = selected_entreprises[0]
entreprise_2 = selected_entreprises[1]
# chemin des entreprises
dossier_1 = f"../data/transformed/{entreprise_1}/"
dossier_2 = f"../data/transformed/{entreprise_2}/"
# je peux alors récupérer les indicateurs associés à chaque entreprise
liste_indic_1 = importation_data(dossier_1, col_inutiles)[1]

liste_indic_2 = importation_data(dossier_2, col_inutiles) [1]
# indicateurs communs
indic_commun = list(set(liste_indic_1) & set(liste_indic_2))

# selection de l'indicateur à comparer
indicateur = st.selectbox(
    "Veuillez choisir un indicateur: ",
    indic_commun,
    index = None
    )
if indicateur:
    data_1 = extraire_indicateur(dossier_1, indicateur)
    data_2 = extraire_indicateur(dossier_2, indicateur)
    data_1["Entreprise"] = entreprise_1
    data_2["Entreprise"] = entreprise_2
    data = pd.concat([data_1, data_2], ignore_index = True)
    
    for col in list(data.columns):
        if col != "Indicateur" and col!= "Année":
            affichage_graphs(True, indicateur, data, "Entreprise", col)
    
    



