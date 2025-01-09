import pandas as pd
import sys
sys.path.append("get_tables_PDF/utils")
from table_viewer import show_table

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

def fill_header(df):
    return True

def unpivot_df(df, nb_headers):
    print(df, "a \n")
    header = df.iloc[:nb_headers]

    # header = fill(header)
    header = header.fillna(method="ffill", axis=1) # Rempli les headers vide par ceux précédent

    df.columns = pd.MultiIndex.from_frame(header.T) # Header en MultiIndex    

    df = df.iloc[2:].reset_index(drop=True)  # Supprimer les lignes d'en-tête originales et réindexer

    df_unpivot = df.melt(id_vars=[df.columns[0]]) # Pivot
    df_unpivot.columns = df_unpivot.columns.astype(str)
    return df_unpivot


data = [
    [None, "Homme", None, "Femme", None],
    [None, "Fonctionnaire", "Non Fonctionnaire", "Fonctionnaire", "Non Fonctionnaire"],
    [2021, 8, 9, 10, 11],
    [2025, 15, 45, 46, 10]
]

data = [
    [None, None, "Homme", None, "Femme", None],
    [None, None, "Fonctionnaire", "Non Fonctionnaire", "Fonctionnaire", "Non Fonctionnaire"],
    [2021, "Catégorie A", 8, 9, 10, 11],
    [2021, "Catégorie B", 15, 25, 20, 30],
    [2021, "Catégorie C", 45, 35, 40, 25],
    [2022, "Catégorie A", 50, 55, 60, 65],
    [2022, "Catégorie B", 70, 75, 80, 85]
]


df = pd.DataFrame(data)
df.columns = df.columns.astype(str)
df = unpivot_df(df, nb_headers=2)

show_table(df)
# print(df)

