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

#----selection Thématique--------
opt_thm = ["absenteisme","condition","droit","effectif","formation","remuneration","handicap","exterieur"]
selection = st.pills("Veuillez choisir une ou plusieurs thématiques à étudier :", opt_thm, selection_mode="multi")

#--IMPORTATION DE LA DATA----------------
if not selection:
    st.write("Veuilliez sélectionner au moins une thématique.")
else:
    for s in selection: 
        file_path="..\\data\\transformed\\EDF\\"+s
    noms_fichiers = [f for f in os.listdir(file_path) if f.endswith('.csv')]
    data = []
    for e in noms_fichiers:
        chemin = os.path.join(file_path,e)
        df = pd.read_csv(chemin, sep=';')
        data.append(df)
    df_concatene = pd.concat(data, ignore_index=True)
    col_inutiles = ["Perimètre juridique","Perimètre spatial","Chapitre du bilan social","Unité","Plage M3E"]
    for colonne in col_inutiles:
        if colonne in df_concatene.columns:
            df_concatene = df_concatene.drop(columns=colonne)
    Edf_data = df_concatene

#----selection d'indicateurs--------

indicateurs = sorted(Edf_data["Indicateur"].unique())

#----selection dimension--------
dimension = Edf_data.select_dtypes(include=["object", "category"]).columns.tolist()
dimension.remove("Indicateur")
dimension.append("Année")

if selection:  
    st.sidebar.subheader("Indicateur")
    indicateur_ = st.sidebar.selectbox(
            "Veuillez choisir un indicateur :",
            indicateurs,
            index=None,
            placeholder="Sélectionnez un indicateur...",
        )
    df = Edf_data[Edf_data["Indicateur"] == indicateur_]
    if indicateur_:
        st.sidebar.subheader("Axes d'analyse")
        dimension.append("Aucune variable")
        dimension_1 = st.sidebar.selectbox("Veuillez choisir le 1er axe d'analyse :",dimension, index=1) 
        #dimension = dimension.remove(dimension_1) 
        dimension_2 = st.sidebar.selectbox("Veuillez choisir le 2eme axe d'analyse :",dimension, index=1) #Valeur année par défaut
        variables=[dimension_1,dimension_2]


#----Actualisation de la data----------------
#---------Filtre de la base de données

##############################################################
#--########-------CREATION DES GRAPHIQUES----######
##############################################################

#----------------Graph univarié-----------------------------
if dimension_1=="Aucune variable":
    st.write("Selectionner les variables/axes d'analyses")
elif dimension_2=="Aucune variable":
    df_grouped = df.groupby(dimension_1, as_index=False).sum()

    fig_bar=px.bar(df_grouped, x=dimension_1, y="Valeur",
                labels={dimension_1, "Valeur :" + indicateur_},
                title=indicateur_ +" des employés par année"
                )

    #  graphique en anneau
    fig_donut = px.pie(df_grouped, names=dimension_1, values="Valeur", 
                    title= indicateur_+" des employés par année", hole=0.6)

    a,b=st.columns(2)
    with a:
        st.plotly_chart(fig_donut)
    with b:
        st.plotly_chart(fig_bar)
else:
#----------------Graph multiple----------------------------

    df_grouped = df.groupby([dimension_1,dimension_2], as_index=False).sum()
    fig_secteur = px.sunburst(df_grouped, path=[dimension_1,dimension_2], values="Valeur",
                    # title=indicateur_+ " des employés par année"
                    )
        
    fig_ligne=px.line(df_grouped, x=dimension_1,
                    y="Valeur",
                    color=dimension_2,
                    labels={dimension_2, "Valeur: "+indicateur_},
                    # title="Evolution des "+ indicateur_+ "des employés par année",
                    color_discrete_sequence=px.colors.qualitative.D3
                    )
        
    fig_bar=px.bar(df_grouped, x=dimension_1,
                y="Valeur",
                color=dimension_2,
                barmode="group",
                labels={dimension_2, "Valeur: "+indicateur_},
            #     title="Evolution des "+ indicateur_+ "des employés par année",
                color_discrete_sequence=px.colors.qualitative.D3  )

    # Créer la carte de chaleur
    map_data = df.pivot_table(values="Valeur", index=dimension_1, columns=dimension_2, aggfunc="sum")
    fig_carte = px.imshow(
        map_data,
        text_auto=True,
        color_continuous_scale="Viridis",
        #title="Carte des valeurs par "+ dimension_1+ " et "+ dimension_2
        )
    
    # Désactiver la barre latérale si nécessaire

    # Créer une grille 2x2 pour afficher les graphiques
    col1, col2 = st.columns(2)

    # Colonne 1 : Secteur et Carte
    with col1:
        with stylable_container(key="graph_container1",
                            css_styles="""{
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                                border-radius: 10px;
                                background-color: #ffffff;
                            }""" ): 
            
            # Titre et graphique Secteur
            #st.markdown("<h3 style='text-align: center; font-size: 16px;'>Secteur</h3>", unsafe_allow_html=True)
            
            st.plotly_chart(
                    fig_secteur.update_layout(
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),  # Légende en haut
                        margin=dict(l=10, r=10, t=0, b=10),  # Marges pour éviter que ça soit trop collé
                        height=300  # Taille réduite du graphique pour qu'il rentre bien
                    ),
                    use_container_width=True
                )
            st.markdown("<br>", unsafe_allow_html=True)  # Espacement entre les graphiques
        with stylable_container(key="graph_container2",
                            css_styles="""{
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                                border-radius: 10px;
                                background-color: #ffffff;
                            }"""):
            # Titre et graphique Carte
            #st.markdown("<h3 style='text-align: center; font-size: 16px;'>Carte</h3>", unsafe_allow_html=True)
            st.plotly_chart(
                fig_carte.update_layout(
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),  # Légende en haut
                    margin=dict(l=10, r=10, t=0, b=10),  # Marges pour éviter que ça soit trop collé
                    height=300  # Taille réduite du graphique pour qu'il rentre bien
                ),
                use_container_width=True
            )

    # Colonne 2 : Ligne et Bar
    with col2:
        with stylable_container(key="graph_container3",
                            css_styles="""{
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                                border-radius: 10px;
                                background-color: #ffffff;
                            }"""):
            # Titre et graphique Ligne
            # st.markdown("<h3 style='text-align: center; font-size: 16px;'>Ligne</h3>", unsafe_allow_html=True)
            st.plotly_chart(
                fig_ligne.update_layout(
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),  # Légende en haut
                    margin=dict(l=10, r=10, t=0, b=10),  # Marges pour éviter que ça soit trop collé
                    height=300  # Taille réduite du graphique pour qu'il rentre bien
                ),
                use_container_width=True
            )

            st.markdown("<br>", unsafe_allow_html=True)  # Espacement entre les graphiques

        with stylable_container(key="graph_container4",
                            css_styles="""{
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                                border-radius: 10px;
                                background-color: #ffffff;
                            }"""):
            # Titre et graphique Bar
            # st.markdown("<h3 style='text-align: center; font-size: 16px;'>Barre</h3>", unsafe_allow_html=True)
            st.plotly_chart(
                fig_bar.update_layout(
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),  # Légende en haut
                    margin=dict(l=10, r=10, t=0, b=10),  # Marges pour éviter que ça soit trop collé
                    height=300  # Taille réduite du graphique pour qu'il rentre bien
                ),
                use_container_width=True
            )


            




#Zone, treemap, ligne, nuage de points et bulles pour la comparaison d'entreprise
