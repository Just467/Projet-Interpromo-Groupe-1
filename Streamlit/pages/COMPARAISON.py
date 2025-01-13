import streamlit as st
import pandas as pd  
import plotly.express as px 

#  Dataframe
df_abs_conge_aut = None
df_abs_mal = None
df_abs_mat_adopt = None
df_abs_pater = None

# Conditions de travail
df_hor_ind = None
df_rep_comp = None
df_sal_inapt_med = None
df_sal_recl_inap = None
df_reduc_coll = None
df_sal_serv_continu_50 = None
df_sal_temps_part_dec = None

# Droit
df_nb_inst_judic = None
df_nb_non_juri = None

#  Effectif
df_demis = None
df_eff = None
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



 #Multiselect pour choisir les entreprises
selected_entreprises = st.multiselect(
    "Sélectionnez les entreprises de votre choix :",
    options=entreprises,
    default=None  # Par défaut, aucune entreprise n'est sélectionnée
)
 
        
themes = ["Condition de travail","Absentéisme", "Droit", "Effectif", "Formation", "Handicap", "Rémunération"]
selection_themes= st.selectbox("Choisissez une thématique: ", themes)
# Déterminer ce qu'il y a à faire à l'intérieur de chaque thèmes !!!!
if selection_themes == "Condition de travail":
    None
 
 # Absentéisme   
elif selection_themes == "Absentéisme":
    conges, maladie, mat_adop, paternite = st.columns(4)
    with conges:
        if st.button("Congés autorisés"):
            None
    with maladie:
        if st.button("Maladies"):
            None
    with mat_adop:
        if st.button("Congés de maternité ou adoption"):
            None
    with paternite:
        if st.button("Congés de paternité"):
            None
        
   # Droit 
elif selection_themes == "Droit":
    instances, nb_recours = st.columns(2)
    with instances:
        if st.button("Instances judiciaires"):
            None
        
    with nb_recours:
        if st.button("Recours non juridictionnels"):
            None
    # Effectif
elif selection_themes == "Effectif":
    eff, demis, embau_mn_25 = st.columns(3)
    with eff:
        if st.button("Effectif"):
            None
    with demis:
        if st.button("Démissions"):
            None
    with embau_mn_25:
        if st.button("Embauches de salariés de moins de 25 ans"):
            None
    # Formation
elif selection_themes == "Formation":
    nb_heures, form_remu, cont_app, cont_pro = st.columns(4)
    with nb_heures:
        if st.button("Heurses de formation"):
            None
    with form_remu:
        if st.button("Formations rémunérées"):
            None
    with cont_app:
        if st.button("Contrats d'apprentissage"):
            None
    with cont_pro:
        if st.button("Contrats de professionnalisation"):
            None
    # Handicap
elif  selection_themes == "Handicap":
    if st.button("Salariés handicapés"):
        if st.button("Salariés handicapés"):
            None
            

else:
    selection_themes == "Rémunération"
    if st.button("Promotions"):
        None


