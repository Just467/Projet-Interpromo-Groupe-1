import pandas as pd
import sys
sys.path.append("scan_pdf/utils")
from table_viewer import show_table



def pivot_table(nb_headers):
    header = df.iloc[:nb_headers]

    # header = fill(header)
    header = header.fillna(method="ffill", axis=1) # Rempli les headers vide par ceux précédent

    df.columns = pd.MultiIndex.from_frame(header.T) # Header en MultiIndex

    df = df.iloc[2:].reset_index(drop=True)  # Supprimer les lignes d'en-tête originales et réindexer

    df_pivot = df.melt(id_vars=[df.columns[0]]) # Pivot

    return df_pivot


data = [
    [None, "Homme", None, "Femme", None],
    [None, "Fonctionnaire", "Non Fonctionnaire", "Fonctionnaire", "Non Fonctionnaire"],
    [2021, 8, 9, 10, 11],
    [2025, 15, 45, 46, 10]
]

df = pd.DataFrame(data)
df.columns = df.columns.astype(str)
show_table(df)
print(df)

