import pandas as pd
import sys
sys.path.append("get_tables_PDF/utils")
from table_viewer import show_table

def is_number_cell(value):
    return True

def is_tidy_df(df):
    is_tidy = None

    return is_tidy

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

    show_table(df)
    
    print(df, "b \n")
    df = df.iloc[2:].reset_index(drop=True)  # Supprimer les lignes d'en-tête originales et réindexer
    print(df, "c \n")
    df_unpivot = df.melt(id_vars=[df.columns[0]]) # Pivot
    df_unpivot.columns = df_unpivot.columns.astype(str)
    show_table(df_unpivot)
    return df_unpivot


data = [
    [None, "Homme", None, "Femme", None],
    [None, "Fonctionnaire", "Non Fonctionnaire", "Fonctionnaire", "Non Fonctionnaire"],
    [2021, 8, 9, 10, 11],
    [2025, 15, 45, 46, 10]
]

df = pd.DataFrame(data)
df = unpivot_df(df, nb_headers=2)

# show_table(df)
# print(df)

