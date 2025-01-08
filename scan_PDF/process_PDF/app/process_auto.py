import pandas as pd

def pivot_table(nb_headers):
    header = df.iloc[:nb_headers]

    # header = fill(header)
    header = header.fillna(method="ffill", axis=1) # Rempli les headers vide par ceux précédent

    df.columns = pd.MultiIndex.from_frame(header.T) # Header en MultiIndex

    df = df.iloc[2:].reset_index(drop=True)  # Supprimer les lignes d'en-tête originales et réindexer

    df_pivot = df.melt(id_vars=[df.columns[0]]) # Pivot

    return df_pivot


data