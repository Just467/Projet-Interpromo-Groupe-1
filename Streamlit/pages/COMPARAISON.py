import streamlit as st
import pandas as pd  
import plotly.express as px 
import os
file_path = "../data/transformed/EDF/"


#  Dataframes
df_abs_conge_aut = pd.read_csv( file_path + "absenteisme/abs_conges_autorises.csv", sep = ";")
df_abs_mal = pd.read_csv(file_path + "absenteisme/abs_maladie.csv", sep = ";")
df_abs_mat_adopt = pd.read_csv(file_path + "absenteisme/abs_mat_adoption.csv", sep  = ";")
df_abs_pater =pd.read_csv(file_path + "absenteisme/abs_paternite.csv", sep = ";")

# Conditions de travail
df_hor_ind = None
df_rep_comp = None
df_sal_inapt_med = None
df_sal_recl_inap = None
df_reduc_coll = None
df_sal_serv_continu_50 = None
df_sal_temps_part_dec = None

# Droit
df_nb_inst_judic = pd.read_csv(file_path + "droit/nb_instances_judiciaires.csv", sep = ";")
df_nb_non_juri =pd.read_csv(file_path + "droit/nb_recours_non_juridictionnels.csv", sep = ";")

#  Effectif
df_demis = pd.read_csv(file_path + "effectif/demissions.csv", sep = ";")
df_eff = pd.read_csv(file_path + "effectif/effectif.csv", sep = ";")
embauches_moins_25 = None

# Exterieur
df_duree_moye = None
df_nb_moy_temp = None
df_sal_det_acc = None
df_sal_det_mob = None
df_stage_sc = None

# Formation
df_heures = None

# Handicap
df_sal_hand = None

# rémunération
df_coll_sup = None


# menu déroulant 

entreprises = ["EDF", "ENGIE", "INSA", "DECATHLON","CNP", "EDF"]
selected_entreprises = []



 #Multiselect pour choisir les entreprises
selected_entreprises = st.multiselect(
    "Sélectionnez les entreprises de votre choix :",
    options=entreprises,
    default=None  # Par défaut, aucune entreprise n'est sélectionnée
)
nom_fichier_to_intitule = {
    "abs_conges_autorises": "Absences pour congés autorisés",
    "abs_maladie": "Absences pour maladie",
    "abs_mat_adoption": "Absences pour congés maternité ou adoption",
    "abs_paternite": "Absences pour congés paternité",
    "sal_services_continus_50plus": "Salariés de plus de 50 ans",
    "nb_instances_judiciaires": "Nombre d'instances judiciaires",
    "nb_recours_non_juridictionnels": "Nombre de recours non juridictionnels",
    "demissions": "Démissions",
    "effectif": "Effectif",
    "embauches_moins25": "Salariés de moins de 25 ans",
    "stagiaires_scolaires": "Stagiaires scolaires",
    "contrats_apprentissage": "Contrats d'apprentissage",
    "contrats_pro": "Contrats de professionnalisation",
    "promo_college_sup": "Promotions",
}
base_path = "../data/transformed"

def charger_csv(nom_entreprise):
    chemin_entreprise = os.path.join(base_path, nom_entreprise)
    entreprise_dataframes = {}
    liste_indicateurs = []
    
    if os.path.exists(chemin_entreprise):
        for root, dirs, files in os.walk(chemin_entreprise):
            for file in files:
                if file.endswith(".csv"):
                    try:
                        # Charger le fichier CSV
                        file_path = os.path.join(root, file)
                        df = pd.read_csv(file_path, sep=";")
                        
                        # Vérifier la colonne "Indicateur"
                        if "Indicateur" in df.columns:
                            indicateur = df["Indicateur"].iloc[0]  # Prendre la première valeur
                            entreprise_dataframes[indicateur] = df
                            
                            # Ajouter l'indicateur à la liste
                            liste_indicateurs.append(indicateur)
                        else:
                            st.error(f"Le fichier {file} ne contient pas de colonne 'Indicateur'.")
                    except Exception as e:
                        st.error(f"Erreur lors du chargement de {file}: {e}")
    else:
        st.error(f"Le répertoire pour {nom_entreprise} n'existe pas.")
    
    return liste_indicateurs, entreprise_dataframes

# Affichage des indicateurs sous forme de liste déroulante
for entreprise in selected_entreprises:
    st.markdown(f"### Indicateurs pour {entreprise}:")
    liste_indicateurs, entreprise_dataframes = charger_csv(entreprise)
    
    if liste_indicateurs:
        # Créer une liste déroulante pour les indicateurs
        choix_indicateur = st.selectbox(
            f"Choisissez un indicateur pour {entreprise}",
            options=liste_indicateurs,
            key=f"{entreprise}_indicateur"
        )
        
        