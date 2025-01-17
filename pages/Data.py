# p2_dataframe_demo

import streamlit as st
import pandas as pd
import numpy as np

####### Brouillon synthèse EDF #########

st.header("Synthèse Diversité & Inclusion")
st.write(" ")

st.subheader("Genre",divider="gray")
col1, col2 = st.columns(2)
with col1:
    st.image("C:\\Users\\Admin\\Documents\\AS 2024 2025\\Deuxième semestre\\Projet inter-promo\\Compil pour synthèse\\Evolution de l'indicateur effectif par année et par genre.png", caption="Evolution de l'indicateur effectif par année et par genre")
with col2: 
    st.write(" ")
    cont = st.container(border=True)
    cont.write(""" <div style='text-align: center;'> <p>Nous observons sur ce graphique, représentant l'évolution du nombre de salariés par genre, qu'il y a nettement plus d'hommes que de femmes.</p> </div> """, unsafe_allow_html=True) 
    cont.write(""" <div style='text-align: center;'> <p>Nous constatons que la parité au sein de l'entreprise n'est pas encore atteinte. Cela pourrait donc constituer un axe de réfléxion au sujet de la politique diversité et inclusion.</p> </div> """, unsafe_allow_html=True)
st.write(" ")

st.subheader("Handicap",divider="gray")
col1, col2 = st.columns(2)
with col2:
    st.image("C:\\Users\\Admin\\Documents\\AS 2024 2025\\Deuxième semestre\\Projet inter-promo\\Compil pour synthèse\\Evolution de l'indicateur salariés en situation de handicap par année.png", caption="Evolution de l'indicateur salariés en situation de handicap par année")
with col1: 
    st.write(" ")
    st.write(" ")
    cont = st.container(border=True)
    cont.write(""" <div style='text-align: center;'> <p>Nous observons sur ce graphique, représentant l'évolution du nombre de salariés en situation de handicap par collège, une nette hausse.</p> </div> """, unsafe_allow_html=True) 
    cont.write(""" <div style='text-align: center;'> <p>Nous constatons que l'inclusion des personnes en situation de handicap s'est nettelemnt améliorée ces dernières années.</p> </div> """, unsafe_allow_html=True)
st.write(" ")

st.subheader("Nationalité",divider="gray")
col1, col2 = st.columns(2)
with col1:
    st.image("C:\\Users\\Admin\\Documents\\AS 2024 2025\\Deuxième semestre\\Projet inter-promo\\Compil pour synthèse\\Evolution de l'indicateur effectif par année par nationalité.png", caption="Evolution de l'indicateur effectif par année par nationalité")
with col2: 
    st.write(" ")
    cont = st.container(border=True)
    cont.write(""" <div style='text-align: center;'> <p>Nous observons sur ce graphique, représentant l'évolution de l'effectif par nationalité, une très légère hausse.</p> </div> """, unsafe_allow_html=True) 
    cont.write(""" <div style='text-align: center;'> <p>Nous constatons que les autres nationalités ne sont pas beacoup représentée au sein de l'entreprise. Cela pourrait donc constituer un axe de réfléxion au sujet de la politique diversité et inclusion.</p> </div> """, unsafe_allow_html=True)

st.subheader("Age",divider="gray")
col1, col2 = st.columns(2)
with col2:
    st.image("C:\\Users\\Admin\\Documents\\AS 2024 2025\\Deuxième semestre\\Projet inter-promo\\Compil pour synthèse\\Evolution de l'indicateur effectif par année et par tranche d'age.png", caption="Evolution de l'indicateur effectif par année et par tranche d'age")
with col1: 
    st.write(" ")
    cont = st.container(border=True)
    cont.write(""" <div style='text-align: center;'> <p>Nous observons sur ce graphique, représentant l'évolution de l'effectif par tranche d'âge, une légère augmentation du nombre de salariés plus agés.</p> </div> """, unsafe_allow_html=True) 
    cont.write(""" <div style='text-align: center;'> <p>Nous constatons que la répartition de l'effectif par tranche d'age évolue assez peu, excepté pour les 25 à 35 ans et les 36 à 45 ans où la tendance semble d'inverser.</p> </div> """, unsafe_allow_html=True)