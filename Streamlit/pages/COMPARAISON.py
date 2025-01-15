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

entreprises = ["EDF", "ENGIE", "INSA", "DECATHLON","CNP"]
selected_entreprises = []

# Liste des indicateurs (n'affiché que si 2 entreprises ou plus sont sélectionnées)
indicateurs = [
        "Absences pour congés autorisés", "Absences pour maladie", "Absences pour congés maternité ou adoption",
        "Absences pour congés paternité", "Salariés de plus de 50 ans", "Nombre d'instances judiciaires",
        "Nombre de recours non juridictionnels", "Démissions", "Effectif", "Salariés de moins de 25 ans",
        "Stagiaires scolaires", "Contrats d'apprentissage", "Contrats de professionnalisation", "Promotions"
    ]




 #Multiselect pour choisir les entreprises
selected_entreprises = st.multiselect(
    "Sélectionnez les entreprises de votre choix :",
    options=entreprises,
    default=None  # Par défaut, aucune entreprise n'est sélectionnée
)

# Affichage d'un message si moins de 2 entreprises sont sélectionnées
if len(selected_entreprises) != 2:
    st.warning("Veuillez sélectionner **exactement deux entreprises** pour choisir un indicateur.")
else:
    
    # Affichage du selectbox pour les indicateurs
    selection_indicateur = st.selectbox(
        "Choisissez un indicateur :",
        options=indicateurs
    )


# Affichage des résultats pour l'indicateur sélectionné (exemple)
    st.write(f"Vous avez sélectionné l'indicateur : **{selection_indicateur}**")
    st.write(f"Comparaison entre les entreprises : {', '.join(selected_entreprises)} en terme de : **{selection_indicateur}**")



 # Logique spécifique pour l'indicateur "Absences pour congés paternité"
    if selection_indicateur == "Absences pour congés paternité":
        # Vérifiez les deux entreprises sélectionnées
        entreprise_1, entreprise_2 = selected_entreprises[:2]

        # Créez des colonnes pour afficher les graphiques côte à côte
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"Résultats pour {entreprise_1}")
            if entreprise_1 == "EDF":
                # Graphiques pour EDF
                df = pd.read_csv("D:/Mon M1/EDF/Projet-Interpromo-Groupe-1/data/transformed/EDF/absenteisme/abs_paternite.csv", sep=";")
                st.header("Nombre Absence pour congé de paternité et d'accueil de l'enfant par Année")
                total_par_année = df.groupby(['Année'])['Valeur'].sum().reset_index()

                # Bar Chart
                fig = px.bar(
                    data_frame=df,
                    x="Année",
                    y="Valeur",
                    title="Graphe: Nombre Absence pour congé de paternité et d'accueil de l'enfant par année"
                )
                st.plotly_chart(fig, use_container_width=True)

                # Line Chart
                fig = px.line(
                    total_par_année,
                    x='Année',
                    y='Valeur',
                    markers=True,
                    title="Évolution du Nombre Absence pour congé de paternité et d'accueil de l'enfant par année",
                    labels={"Valeur": "Nombre Absence pour congé de paternité et d'accueil de l'enfant"},
                )
                st.plotly_chart(fig, use_container_width=True)

            elif entreprise_1 == "INSA":
                # Graphiques pour INSA
                df = pd.read_csv("D:/Mon M1/EDF/Projet-Interpromo-Groupe-1/data/transformed/EDF/effectif/embauches_moins25.csv", sep=";")
                st.header("Nombre Embauches de salariés de moins de 25 ans par Année et Genre")
                total_par_année_genre = df.groupby(['Année', 'Genre'])['Valeur'].sum().reset_index()

                # Bar Chart
                fig = px.bar(
                    total_par_année_genre,
                    x='Année',
                    y='Valeur',
                    color='Genre',
                    barmode='group',  # Barres groupées par genre
                    title="Graphe: Nombre Embauches de salariés de moins de 25 ans par année et genre",
                )
                st.plotly_chart(fig, use_container_width=True)

                # Line Chart
                fig = px.line(
                    total_par_année_genre,
                    x='Année',
                    y='Valeur',
                    color='Genre',
                    markers=True,
                    title="Évolution du Nombre Embauches de salariés de moins de 25 ans par année et genre",
                    labels={"Valeur": 'Nombre Embauches de salariés de moins de 25 ans'},
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader(f"Résultats pour {entreprise_2}")
            if entreprise_2 == "EDF":
                # Graphiques pour EDF
                df = pd.read_csv("D:/Mon M1/EDF/Projet-Interpromo-Groupe-1/data/transformed/EDF/absenteisme/abs_paternite.csv", sep=";")
                st.header("Nombre Absence pour congé de paternité et d'accueil de l'enfant par Année")
                total_par_année = df.groupby(['Année'])['Valeur'].sum().reset_index()

                # Bar Chart
                fig = px.bar(
                    data_frame=df,
                    x="Année",
                    y="Valeur",
                    title="Graphe: Nombre Absence pour congé de paternité et d'accueil de l'enfant par année"
                )
                st.plotly_chart(fig, use_container_width=True)

                # Line Chart
                fig = px.line(
                    total_par_année,
                    x='Année',
                    y='Valeur',
                    markers=True,
                    title="Évolution du Nombre Absence pour congé de paternité et d'accueil de l'enfant par année",
                    labels={"Valeur": "Nombre Absence pour congé de paternité et d'accueil de l'enfant"},
                )
                st.plotly_chart(fig, use_container_width=True)

            elif entreprise_2 == "INSA":
                # Graphiques pour INSA
                df = pd.read_csv("D:/Mon M1/EDF/Projet-Interpromo-Groupe-1/data/transformed/EDF/effectif/embauches_moins25.csv", sep=";")
                st.header("Nombre Embauches de salariés de moins de 25 ans par Année et Genre")
                total_par_année_genre = df.groupby(['Année', 'Genre'])['Valeur'].sum().reset_index()

                # Bar Chart
                fig = px.bar(
                    total_par_année_genre,
                    x='Année',
                    y='Valeur',
                    color='Genre',
                    barmode='group',  # Barres groupées par genre
                    title="Graphe: Nombre Embauches de salariés de moins de 25 ans par année et genre",
                )
                st.plotly_chart(fig, use_container_width=True)

                # Line Chart
                fig = px.line(
                    total_par_année_genre,
                    x='Année',
                    y='Valeur',
                    color='Genre',
                    markers=True,
                    title="Évolution du Nombre Embauches de salariés de moins de 25 ans par année et genre",
                    labels={"Valeur": 'Nombre Embauches de salariés de moins de 25 ans'},
                )
                st.plotly_chart(fig, use_container_width=True)