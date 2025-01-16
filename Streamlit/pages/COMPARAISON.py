import pandas as pd
import streamlit as st

# Liste des entreprises disponibles pour comparaison
entreprises = ["ENGIE", "INSA", "CNP"]

# Interface utilisateur
st.title("Comparaison d'indicateurs entre EDF et une autre entreprise")

# Étape 1 : Sélection d'une entreprise autre qu'EDF
selected_entreprise = st.selectbox(
    "Sélectionnez une entreprise à comparer avec EDF :",
    entreprises
)

# Étape 2 : Gestion des indicateurs et fichiers CSV pour chaque entreprise
if selected_entreprise:
    if selected_entreprise == "ENGIE":
        indicateurs_entreprise = {
            "Salariés en situation de handicap": "../data/transformed/ENGIE/handicap/nombre_handicapés.csv",
            "effectif": "../data/transformed/ENGIE/emploi/effectif.csv",
        }
        indicateurs_edf = {
            "Salariés en situation de handicap": "../data/transformed/EDF/handicap/sal_handicap.csv",
            "effectif": "../data/transformed/EDF/effectif/effectif.csv",
        }

    elif selected_entreprise == "INSA":
        indicateurs_entreprise = {
            "Masse salariale": "../data/transformed/INSA/rémunération/masse_salariale.csv",
            "Nombre de Promotion": "../data/transformed/INSA/mouvement_et_carrière/nombre_promotions.csv",
        }
        indicateurs_edf = {
            "Masse salariale": "../data/transformed/EDF/remuneration/masse_salariale_annuelle.csv",
            "Nombre de Promotion": "../data/transformed/EDF/remuneration/promo_college_sup.csv",
        }

    elif selected_entreprise == "CNP":
        indicateurs_entreprise = {
            "Salariés en situation de handicap": "../data/transformed/ENGIE/handicap/nombre_handicapés.csv",
        }
        indicateurs_edf = {
            "Salariés en situation de handicap": "../data/transformed/EDF/handicap/sal_handicap.csv",
        }

    else:
        st.error("Entreprise non reconnue.")

    # Étape 3 : Sélection de l'indicateur à comparer
    indicateur_selectionne = st.selectbox(
        "Choisissez un indicateur :",
        list(indicateurs_entreprise.keys())
    )

    # Étape 4 : Charger les données, corriger et afficher les résultats
    if indicateur_selectionne:
        try:
            # Charger les fichiers CSV pour EDF et l'entreprise sélectionnée
            fichier_entreprise = indicateurs_entreprise[indicateur_selectionne]
            fichier_edf = indicateurs_edf[indicateur_selectionne]

            # Charger les données avec correction d'encodage
            df_entreprise = pd.read_csv(fichier_entreprise, sep=";", encoding="latin1")
            df_edf = pd.read_csv(fichier_edf, sep=";", encoding="latin1")

            # Renommer les colonnes pour EDF (problème d'encodage)
            df_edf.rename(columns={
                "AnnÃ©e": "Année",
                "Valeur": "Valeur"
            }, inplace=True)

            # Vérifier et filtrer pour l'indicateur choisi
            if "Indicateur" in df_entreprise.columns:
                df_entreprise = df_entreprise[df_entreprise["Indicateur"] == indicateur_selectionne]

            if "Indicateur" in df_edf.columns:
                df_edf = df_edf[df_edf["Indicateur"] == indicateur_selectionne]

            # Vérifier la présence des colonnes nécessaires
            if {"Année", "Valeur"}.issubset(df_entreprise.columns) and {"Année", "Valeur"}.issubset(df_edf.columns):
                # Afficher les données
                st.subheader(f"Indicateur sélectionné : {indicateur_selectionne}")
                st.write(f"**Données pour {selected_entreprise}**")
                st.write(df_entreprise[["Année", "Valeur"]])

                st.write(f"**Données pour EDF**")
                st.write(df_edf[["Année", "Valeur"]])

            else:
                st.error("Les colonnes nécessaires ('Année', 'Valeur') sont absentes des fichiers après filtrage.")
        except Exception as e:
            st.error(f"Erreur lors du chargement des données : {e}")
