import streamlit as st
from utils import importation_data, selection_menu, affichage_graphs
import os
import pandas as pd
'''


dict_indicateurs_communs = {
    ("EDF", "ENGIE") : [ "Démissions", "Stagiaires scolaires"],
    ("EDF", "INSA"): ["Salariés en situation de handicap"],
    ("EDF", "EDF"): ["Absence pour congés autorisés"]
}


def selection(dossier_entreprise_1, dossier_entreprise_2, col_inutiles, dimension):
    entreprises = list(set([entreprise for duo in dict_indicateurs_communs.keys() for entreprise in duo]))
    
    st.subheader("Sélection des entreprises")
    entreprises_selectionnees = st.multiselect(
        "Veuillez choisir deux entreprises: ",
        entreprises,
        default = None,
        max_selections = 2
    )
    
    if not entreprises_selectionnees or len(entreprises_selectionnees) != 2:
        st.warning("Veuillez sélectionner exactement deux entreprises.")
        return(None, None, None, None)
    
    dossier_entreprise_1, dossier_entreprise_2 = entreprises_selectionnees
    duo_selectionne = tuple(sorted(entreprises_selectionnees))
    
    # vérif  des indicateurs en commun
    
    if duo_selectionne not in dict_indicateurs_communs:
        st.error("Aucun indicateur commun trouvé pour ces deux entreprises.")
        return (None, None, None,None)
    
    indicateurs_communs = dict_indicateurs_communs[duo_selectionne]
    
    # selection d'un indicateur
    
    st.subheader("Indicateur")
    indicateur_ = st.selectbox(
        "Veuillez choisir un indicateur en commun:",
        sorted(indicateurs_communs),
        index = 0
        
    )
    
    if not indicateur_:
        st.warning("Veuillez sélectionner un indicateur.")
        return(None, None, None, None,None)
    
    def charger_donnees(dossier, indicateur):
        sous_dossiers = [nom for nom in os.listdir(dossier) if os.path.isdir(os.path.join(dossier, nom))]
        data = []
        
        for sous_dossier in sous_dossiers:
            file_path = os.path.join(dossier, sous_dossier)
            fichiers_csv = [f for f in os.listdir(file_path) if f.endswith('.csv')]
            
            for fichier in fichiers_csv:
                chemin = os.path.join(file_path, fichier)
                df = pd.read_csv(chemin, sep = ";")
                if "Indicateur" in df.columns and indicateur in df["Indicateur"].values:
                    data.append()
                    
        if data:
            df_concatene = pd.concat(data, ignore_index = True)
            for colonne in col_inutiles:
                if colonne in df_concatene.columns:
                    df_concatene = df_concatene.drop(columns = colonne)
                
            return df_concatene[df_concatene["Indicateur"] == indicateur]
        else:
            return pd.DataFrame()
    
    df_1 = charger_donnees(dossier_entreprise_1, indicateur_)
    df_2 = charger_donnees(dossier_entreprise_2, indicateur_)


    if df_1.empty or df_2.empty:
        st.error("Impossible de charger les données pour cet indicateur.")
        return(None, None, None, None)
    
    if dimension not in df_1.columns or dimension not in df_2.columns:
        st.error(f"La dimension {dimension} n'est pas disponible pour les deux entreprises")
        return(None, None, None, None)
    
    df_1_filtered = df_1[[dimension, "Indicateur"]].copy()
    df_2_filtered = df_2[[dimension, "Indicateur"]].copy()
    
    return (entreprises_selectionnees, indicateur_, df_1_filtered, df_2_filtered)


selection_entr, indicateur, df_entreprise_1, df_entreprise_2 = selection(
    dossier_entreprise_1="../data/transformed/EDF/",
    dossier_entreprise_2="../data/transformed/EDF/",
    col_inutiles=["Perimètre juridique","Perimètre spatial","Chapitre du bilan social","Unité","Plage M3E"],
    dimension="Année"
)

    
if selection_entr and indicateur and not df_entreprise_1.empty and not df_entreprise_2.empty:
    st.write(f"Comparaison des entreprises {selection[0]} et {selection[1]} sur l'indicateur {indicateur} par la dimension {dimension}.")
    st.write("Données Entreprise 1 :")
    st.dataframe(df_entreprise_1)
    st.write("Données Entreprise 2 :")
    st.dataframe(df_entreprise_2)
else:
    st.write("Aucune comparaison possible avec les critères sélectionnés.")       

'''


data = pd.read_csv("/home/sid2018-3/Téléchargements/brouillon comparaison handicap.csv", sep=';')
affichage_graphs (True, "Salariés en situation de handicap", data, "Entreprise", None)
# True: suppose 
# None: 