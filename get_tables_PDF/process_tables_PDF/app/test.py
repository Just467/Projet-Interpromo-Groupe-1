
from functions_process_tables_PDF import *

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
    [None, "categ", "Fonctionnaire", "Non Fonctionnaire", "Fonctionnaire", "Non Fonctionnaire"],
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
dataframes.append(pd.DataFrame(data4))

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

processed_data = {}
for idx, df in enumerate(dataframes):
    processed_df = process_tables([df])

    processed_data[idx] = {
            "raw_df": df,
            "processed_df": processed_df
        }
    
show_processed_dataframes(processed_data)
