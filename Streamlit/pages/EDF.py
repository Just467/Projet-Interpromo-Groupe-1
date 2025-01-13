import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container
# Mise en forme avec Streamlit Extras pour ajouter des bordures, etc.
import streamlit_extras 

st.set_page_config(layout="wide")  # Utiliser toute la largeur de l'écran


#--IMPORTATION DE LA DATA----------------
file_path="E:/perso/Année scolaire 2024-2025/Cours/PIP/Projet-Interpromo-Groupe-1/data/transformed/EDF/"
EDF_data1 = pd.read_csv(file_path+"effectif/effectif.csv", sep=";")
EDF_data2 = pd.read_csv(file_path+"effectif/demissions.csv", sep=";")
EDF_data3 = pd.read_csv(file_path+"effectif/embauches_moins25.csv", sep=";")

#Traitement de la data
Edf_data = pd.concat([EDF_data1, EDF_data2, EDF_data3], ignore_index=True)
Edf_data = Edf_data.drop(columns=["Perimètre juridique","Perimètre spatial","Plage M3E","Unité"])


#----selection Thématique (Emeline)--------
thematique=["a","b","c"]
#----selection d'indicateurs (Emeline)--------
indicateur_ = st.sidebar.selectbox("Indicateur :", sorted(Edf_data["Indicateur"].unique()), index=1)
df = Edf_data[Edf_data["Indicateur"] == indicateur_]
#----selection dimension (Emeline)--------
dimension = Edf_data.select_dtypes(include=["object", "category"]).columns.tolist()
dimension.append("Année")
dimension_1 = st.sidebar.selectbox("Var 1 :",["Aucune variable"]+ dimension, index=1) 
dimension_2 = st.sidebar.selectbox("Var 2 :",["Aucune variable"]+dimension, index=1) #Valeur année par défaut
dimension_3 = st.sidebar.selectbox("Var 3 :",["Aucune variable"]+ dimension, index=1) 
variables=[dimension_1,dimension_2,dimension_3]
#----Actualisation de la data----------------
#---------Filtre de la base de données

##############################################################
#--########-------CREATION DES GRAPHIQUES----######
##############################################################
#---------- Indicateur--------------------------
a,b,c,d=st.columns(4)
with a:
    st.metric("Minimum", int(df["Valeur"].min()), delta=None)
with b:
    st.metric("Moyenne", int(df["Valeur"].mean()), delta=None)
with c:
    st.metric("Maximum", int(df["Valeur"].max()), delta=None)
with d:
    st.metric("Total", int(df["Valeur"].sum()), delta=None)
style_metric_cards()



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