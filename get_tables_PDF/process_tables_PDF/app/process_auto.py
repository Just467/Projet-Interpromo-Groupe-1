import pandas as pd
import sys
sys.path.append("get_tables_PDF/utils")
from dataframe_viewer import show_dataframes

boolean = True

def is_number_cell(value):
    return True

def is_header(series):
    # regarder premier mot / deuxième mot si en lien avec les autres
    # ignorer peut-être le premier mot ? pas forcément
    # presence de nan
    return boolean

def is_variable(series):
    # regarder si premier mot / en lien avec les autres
    
    return boolean

def format_df(df):
    """
    Formate simplement une DataFrame en supprimant les lignes et colonnes vides, 
    convertissant toutes les valeurs et colonnes en chaînes de caractères, 
    et en supprimant les espaces.
    
    args: 
        df (DataFrame): df à formater

    return:
        DataFrame: df formatée
    """
    # Supprimer colonnes et lignes totales
    # si plus d'élements en bas que en haut que à droite => colonnes
    # si plus d'éléments en 

    # Supprime les lignes et colonnes entièrement vides
    df = df.dropna(how='all', axis=0)
    df = df.dropna(how='all', axis=1)

    # Converti toutes les valeurs en str et supprime les espaces
    df = df.applymap(lambda x: str(x).replace(" ", "") if pd.notnull(x) else "")

    # Supprime tous les espaces des noms de colonnes
    df.columns = [str(col).replace(" ", "") for col in df.columns]

    return df

def fill_header(header):
    filled_header = header.fillna(method="ffill", axis=1).fillna("unknown")
    return filled_header

def clean_multi_index(multi_index):
    """
    Ajoute un suffixe `_i` aux éléments du MultiIndex pour rendre chaque tuple unique.

    :param multi_index: MultiIndex à transformer.
    :return: MultiIndex avec des tags uniques appliqués de manière cohérente par tuple.
    """

    def unique_suffix(val, count):
        return f"{val}_{count}" if count > 0 else val
    
    tuple_counts = {} # Stocke le nb de fois qu'un tuple est vu
    new_tuples = [] # Stocke les nouveaux tuples retrournés

    # Parcoure chaque tuple dans le MultiIndex
    for tuple in multi_index:
        if tuple not in tuple_counts:
            tuple_counts[tuple] = 0
        else:
            tuple_counts[tuple] += 1
        
        new_tuple = []
        for val in tuple:
            count = tuple_counts.get(tuple, 0)
            new_tuple.append(unique_suffix(val, count))
        
        new_tuples.append(new_tuple)

    return pd.MultiIndex.from_tuples(new_tuples)



def unpivot_df(df, nb_categ_headers, nb_variables, value_colname):
    """
    Transforme un DataFrame avec plusieurs en-têtes en un DataFrame au format "tidy".
    
    :param df: DataFrame brut à transformer.
    :param nb_categ_headers: Nombre de lignes d'en-tête à utiliser pour le MultiIndex.
    :return: DataFrame au format "tidy".
    """

    if nb_categ_headers == 0:
        return df
    
    # Extraire les lignes d'en-tête
    header = df.iloc[:nb_categ_headers]

    # Remplir les valeurs manquantes horizontalement
    header = fill_header(header)

    # Crée le MultiIndex (en-têtes)
    df.columns = pd.MultiIndex.from_frame(header.T)
    df.columns = clean_multi_index(df.columns)

    # Réinitialise l'index
    df = df.iloc[nb_categ_headers:].reset_index(drop=True)

    variables_cols = df.columns.tolist()[:nb_variables]
    values_cols = df.columns.tolist()[nb_variables:]

    # Dépivote toutes les colonnes sauf celles considérées comme des variables
    df_unpivot = df.melt(id_vars=variables_cols, value_vars=values_cols, value_name=value_colname)

    return df_unpivot



# data = [
#     [None, "Homme", None, "Femme", None],
#     [None, "Fonctionnaire", "Non Fonctionnaire", "Fonctionnaire", "Non Fonctionnaire"],
#     [2021, 8, 9, 10, 11],
#     [2025, 15, 45, 46, 10]
# ]

import pandas as pd

# Générer une liste de DataFrames avec différentes configurations
dataframes = []

# Exemple 1 : Deux en-têtes, plusieurs variables
data1 = [
    [None, None, "Homme", None, "Femme", None],
    [None, None, "Fonctionnaire", "Non Fonctionnaire", "Fonctionnaire", "Non Fonctionnaire"],
    [2021, "Catégorie A", 8, 9, 10, 11],
    [2021, "Catégorie B", 15, 25, 20, 30],
    [2021, "Catégorie C", 45, 35, 40, 25],
    [2022, "Catégorie A", 50, 55, 60, 65],
    [2022, "Catégorie B", 70, 75, 80, 85]
]
dataframes.append(pd.DataFrame(data1))

# Exemple 2 : Une seule en-tête, plusieurs variables
data2 = [
    ["année", "Homme", "Femme"],
    [2021, 8, 10],
    [2022, 15, 25]
]
dataframes.append(pd.DataFrame(data2))

# Exemple 3 : Deux en-têtes, une seule variable
data3 = [
    [None, "Population"],
    ["Homme", 8],
    ["Femme", 10]
]
dataframes.append(pd.DataFrame(data3))

# Exemple 4 : Une seule en-tête, une seule variable
data4 = [
    ["Année", "Population"],
    [2021, 18],
    [2022, 20]
]
# dataframes.append(pd.DataFrame(data4))

# Exemple 5 : Trois en-têtes, plusieurs variables
data5 = [
    [None, None, "Homme", None, "Femme", None],
    [None, None, "Fonctionnaire", "Non Fonctionnaire", "Fonctionnaire", "Non Fonctionnaire"],
    [None, None, "Salaire Moyen", "Salaire Moyen", "Salaire Moyen", "Salaire Moyen"],
    [2021, "Catégorie A", 8, 9, 10, 11],
    [2021, "Catégorie B", 15, 25, 20, 30],
    [2022, "Catégorie A", 50, 55, 60, 65],
    [2022, "Catégorie B", 70, 75, 80, 85]
]
dataframes.append(pd.DataFrame(data5))

# Exemple 6 : Une seule en-tête, trois variables
data6 = [
    ["Année", "Catégorie", "Population"],
    [2021, "Catégorie A", 18],
    [2021, "Catégorie B", 20],
    [2022, "Catégorie A", 22],
    [2022, "Catégorie B", 24]
]

# dataframes.append(pd.DataFrame(data6))
nb = [[2, 2], [0, 1], [1, 1], [3, 2]]

dfs = []
for i in range(len(dataframes)):
    nb_categ_headers=nb[i][0]
    nb_variables=nb[i][1]

    df = dataframes[i]
    df_unpivot = unpivot_df(df, nb_categ_headers=nb_categ_headers, nb_variables=nb_variables, value_colname="valeur")
    dfs.append(df_unpivot)

show_dataframes(dataframes, dfs)
# print(df)

