#Pour l'exécution : (python -m)streamlit run dasbboard_pip.py
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
#import pandas_profiling #creation automatique de profile
#from streamlit_pandas_profiling import st_profile_report
"""
pr = df.profile_report()
st_profile_report(pr)
"""




# Données pour le DataFrame
data = {
    "Nom": ["Alice", "Bob", "Charlie", "Diana", "Ethan"],        
    "Age": [25, 32, 28, 35, 22],                                
    "Ville": ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"], 
    "Score": [88.5, 72.0, 91.0, 67.5, 78.0],                    
    "Adhérent": [True, False, True, False, True],              
    "Catégorie": ["A", "B", "A", "C", "B"]                      
}

# Création du DataFrame
df = pd.DataFrame(data)

# Afficher le DataFrame
print(df)

#--------TITRE+DATA------------------
"""
st.title("Ma première page")
st.subheader("Un sous titre")
st.caption("Ma base de données")
st.write(df)
"""

#--------DATA+_GRAPH------------------
st.title("Ma deuxième page")
st.divider()
st.header("Affichage sous forme de tableau")
st.caption("Ma base de données")
st.write(df)
st.divider()

st.subheader("Affichage sous forme de graph")
import pandas as pd
import plotly.express as px
import streamlit as st

#-----------------------------------
# Graphique linéaire avec Plotly Express
ma_line = px.line(
    df,
    x="Score",
    y="Catégorie",
    color="Catégorie",  # Colonne utilisée pour différencier par couleur
    labels={"Age": "Âge (ans)", "Score": "Points obtenus"},  # Étiquettes personnalisées
    title="chart 1: en ligne"  
)

# Afficher le graphique dans Streamlit
st.plotly_chart(ma_line)

#-----------------------------------
# Graphique en bar

ma_bar = px.bar(
    df,
    x="Age",
    y="Score",
    #color="Catégorie",  # Colonne utilisée pour différencier par couleur
    labels={"Age": "Âge (ans)", "Score": "Points obtenus"},  # Étiquettes personnalisées
    title="chart 1: en ligne"  
)

# Afficher le graphique dans Streamlit
st.plotly_chart(ma_bar)

#-----------------------------------

# Graphique en secteur

ma_pie = px.pie(
    df,
    names="Catégorie",  
    values="Score",  
    title="chart 3: en secteur"  
)

# Afficher le graphique dans Streamlit
st.plotly_chart(ma_pie)

st.divider()


#--------GRAPH+WIDGET------------------


option = st.selectbox(
    'Which number do you like best?',
     df['Catégorie'])

st.write('You selected:', option)
#--------bar laterale plusieurs pages------------------


#--------PLUSIEURS GRAPHES-------------------------------



#-------ANALYSE COMPARATIVE

