import pandas as pd
import streamlit as st
from utils import affichage_graphs  # Import de la fonction pour afficher les graphiques

# Liste des entreprises disponibles pour comparaison
entreprises = ["ENGIE", "INSA", "CNP"]

# Interface utilisateur
st.title("Comparaison des entreprises avec EDF")

# Étape 1 : Sélection d'une entreprise autre qu'EDF
selected_entreprise = st.selectbox(
    "Sélectionnez une entreprise à comparer avec EDF :",
    entreprises
)

# Dictionnaire de correspondance des noms d'indicateurs
correspondance_indicateurs = {
    "Salariés en situation de handicap": ["Nombre de personnes handicapées", "Travailleurs en situation de handicap"],
    "Effectif": ["Effectif"],
    "Masse salariale annuelle": ["Masse salariale"],
    "Promotion dans un collège supérieur": ["Nombre de promotions"]
}

# Fonction pour trouver les indicateurs communs
def trouver_indicateurs_communs(indicateurs_edf, indicateurs_entreprise):
    indicateurs_communs = {}
    for edf_indicateur, autres_indicateurs in correspondance_indicateurs.items():
        # Vérifiez si l'un des noms d'indicateurs correspond
        for indicateur in autres_indicateurs:
            if indicateur in indicateurs_entreprise:
                indicateurs_communs[edf_indicateur] = indicateurs_entreprise[indicateur]
    return indicateurs_communs

# Étape 2 : Gestion des indicateurs et fichiers CSV pour chaque entreprise
if selected_entreprise:
    if selected_entreprise == "ENGIE":
        indicateurs_entreprise = {
            "Nombre de personnes handicapées": "data/transformed/ENGIE/handicap/nombre_handicapés.csv",
            "Effectif": "data/transformed/ENGIE/emploi/effectif.csv",
        }
        indicateurs_edf = {
            "Salariés en situation de handicap": "data/transformed/EDF/handicap/sal_handicap.csv",
            "Effectif": "data/transformed/EDF/effectif/effectif.csv",
        }

    elif selected_entreprise == "INSA":
        indicateurs_entreprise = {
            "Masse salariale": "data/transformed/INSA/rémunération/masse_salariale.csv",
            "Nombre de promotions": "data/transformed/INSA/mouvement_et_carrière/nombre_promotions.csv",
        }
        indicateurs_edf = {
            "Masse salariale annuelle": "data/transformed/EDF/remuneration/masse_salariale_annuelle.csv",
            "Promotion dans un collège supérieur": "data/transformed/EDF/remuneration/promo_college_sup.csv",
        }

    elif selected_entreprise == "CNP":
        indicateurs_entreprise = {
            "Travailleurs en situation de handicap": "data/transformed/CNP/emploi/nombre_travailleurs_handicap.csv",
        }
        indicateurs_edf = {
            "Salariés en situation de handicap": "data/transformed/EDF/handicap/sal_handicap.csv",
        }

    else:
        st.error("Entreprise non reconnue.")

    # Trouver les indicateurs communs
    indicateurs_communs = trouver_indicateurs_communs(indicateurs_edf, indicateurs_entreprise)

    # Étape 3 : Sélection de l'indicateur à comparer
    if indicateurs_communs:
        indicateur_selectionne = st.selectbox(
            "Choisissez un indicateur :",
            list(indicateurs_communs.keys())
        )

        # Étape 4 : Charger les fichiers CSV correspondants
        if indicateur_selectionne:
            fichier_edf = indicateurs_edf[indicateur_selectionne]
            fichier_entreprise = indicateurs_communs[indicateur_selectionne]

            try:
                # Charger les données des fichiers sélectionnés
                data_edf = pd.read_csv(fichier_edf, sep=';', encoding='utf-8')
                data_entreprise = pd.read_csv(fichier_entreprise, sep=';', encoding='utf-8')

                # Ajouter une colonne pour identifier les entreprises
                data_edf["Entreprise"] = "EDF"
                data_entreprise["Entreprise"] = selected_entreprise

                # Combiner les données des deux entreprises
                data_combine = pd.concat([data_edf, data_entreprise], ignore_index=True)

                # Étape 5 : Représentation graphique
                st.header(f"Comparaison de l'indicateur : {indicateur_selectionne}")
                if (selected_entreprise == 'ENGIE' and indicateur_selectionne == 'Effectif') or \
                    (selected_entreprise == 'CNP' and indicateur_selectionne == 'Salariés en situation de handicap') :
                    dim2 = st.sidebar.selectbox("Selectionner un axe d'analsye", [None, 'Genre'])
                else :
                    dim2 = None
                affichage_graphs(True, indicateur_selectionne, data_combine, "Entreprise", dim2)  # Comparaison sans catégorie

            except Exception as e:
                st.error(f"Erreur lors du chargement des données : {e}")
    else:
        st.warning("Aucun indicateur commun trouvé.")
