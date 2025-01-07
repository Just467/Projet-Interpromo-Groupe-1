import pandas as pd

#Fonction Pour supprimer les colones en doublon:

def supprimer_doublons_colonnes(dataframe, colonnes_a_supprimer):
    
    # Supprimer les colonnes spécifiées
    dataframe = dataframe.drop(columns=colonnes_a_supprimer)
    return dataframe
    
# DataFrame concernée
df = pd.read_csv("Mon Nettoyage/bilan-social-d-edf-sa-absenteisme.csv", sep=";")
#df = pd.read_csv("Mon Nettoyage/bilan-social-d-edf-sa-effectifs-et-repartition-par-age-statut-et-sexe.csv", sep = ";")
# df = pd.read_csv("Mon Nettoyage/bilan-social-d-edf-sa-salaries-en-situation-de-handicap.csv", sep=";")
# df = pd.read_csv("Mon Nettoyage/bilan-social-d-edf-sa-travailleurs-exterieurs.csv", sep = ";")

# Colonnes à supprimer
colonnes_doublons = ['Spatial perimeter', 'Indicator', 'Type of contract','Employee category', 'Gender', 'Unit']
# colonnes_doublons = ['Spatial perimeter','Indicator', 'Type of contract', 'Employee category', 'Employee subcategory', 'Gender','M3E classification','Nationality', 'Seniority', 'Age bracket', 'Unit' ], axis=1)

# colonnes_doublons = ['Spatial perimeter','Indicator', 'Type of contract', 'Employee category', 'Gender', 'Unit'], axis=1)
# colonnes_doublons = ['Spatial perimeter','Indicator', 'Employee category', 'Gender', 'Unit'], axis=1)

# Appel de la fonction
df_nettoye = supprimer_doublons_colonnes(df, colonnes_doublons)

print(df_nettoye)

