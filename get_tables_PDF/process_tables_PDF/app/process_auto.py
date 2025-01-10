import pandas as pd
import sys
import re
import numpy as np
sys.path.append("get_tables_PDF/utils")
from dataframe_viewer import show_dataframes
from processed_dataframe_viewer import show_processed_dataframes

boolean = True

# si "Total" dans un header => supprimer colonne
# si "Total" dans une ligne => supprimer ligne

# liste des functions

def format_df(df):
    """
    Formate la DataFrame en supprimant les lignes et colonnes vides, 
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
    df = df.map(lambda x: str(x).replace(" ", "") if pd.notnull(x) else "")

    return df


def is_numerical(value):
    """
    Renvoie True si `value` est considéré numérique càd,
    qui ne contient que des chiffres, points, virgules, devise

    args:
        value (String): obtenue dans chaque élément d'une Series
    return:
        Boolean
    """
    # Traiter d'autres cas comme '30ans' etc... != '>30ans'
    pattern = r"^[\d.,%€$£₹]*$"
    return bool(re.match(pattern, value))


def has_numerical_values(series):
    """
    Renvoie True si la ligne possède une ou plusieurs valeurs dites numériques

    args:
        series (pd.Series)
    return:
        Boolean
    """
    for value in series:
        if is_numerical(value):
            return True
        
    return False


def has_year_sequency(series, series_index, min_year=2020, max_year=2025):
    # Implémenter en PLUS: voir si la date est avant des non numerical pour une seule date)
    # Toujours garder si index == 0
    """
    Renvoie True si la pd.Series contient uniquement des années compris dans la plage
    Avec des règles supplémentaires si c'est la première ligne de la DataFrame
    
    args:
        series (pd.Series): une ligne de DataFrame
        series_index (int): index de la series (ligne/colonne) dans la DataFrame
        min_year (int): année minimale autorisée
        max_year (int): année maximale autorisée
    return:
        bool: True si toutes les valeurs numériques sont dans la plage (ou si une seule année avec row_index=0), sinon False.
    """
    # Vérifie si la valeur est un nombre entier
    def is_pure_number(value):
        return re.match(r"^\d+$", str(value).strip()) is not None

    # Liste des valeurs entières
    int_values = [int(value) for value in series if is_pure_number(value)]

    # Cas où il y a une seule année (peut-être une année ou un nombre par malchance)
    if len(int_values) == 1:
        # True si row_index == 0 et que l'année est dans la plage
        return series_index == 0 and min_year <= int_values[0] <= max_year

    # Vérifie si toutes les valeurs sont dans la plage spécifiée
    return all(min_year <= num <= max_year for num in int_values)



def is_value(series, series_index):
    """
    Renvoie True si la series est considérée comme valeurs
    sinon c'est soit une en-tête soit une variable

    args:
        series (Series): series obtenue en parcourant la DataFrame (ligne/colonne)
    return:
        Boolean
    """
    isValue = True

    if (not has_numerical_values(series)) or (has_year_sequency(series, series_index)):
        isValue = False

    return isValue

# Si headers séparés => créer plusieurs df


def detect_structure(df):
    """
    Renvoie la structure de la df en précisant:
    où se trouvent les headers (en-têtes) et les variables via leur index

    args:
        df (pd.DataFrame)
    return
        dict
    """

    header_indexes = []
    for row_index, row in df.iterrows():
        if not is_value(row, row_index):
            header_indexes.append(row_index)
    
    variable_indexes = []
    for col_index in range(df.shape[1]):  # Itération sur les indices numériques des colonnes
        column = df.iloc[:, col_index]   # Accès à la colonne par index numérique
        if not is_value(column, col_index):
            variable_indexes.append(col_index)
    
    structure = {
        "headers": header_indexes,
        "variables": variable_indexes
    }

    return structure


def add_header(df, missing_label="unknown"):
    """
    Ajoute une ligne tout en haut du DataFrame avec le label spécifié
    
    Args:
        df (pd.DataFrame): Le DataFrame d'origine.
        label (str): Le label à remplir dans la ligne ajoutée.
    Returns:
        pd.DataFrame: Le DataFrame modifié.
    """
    structure = detect_structure(df)
    nb_headers = len(structure["headers"])

    if nb_headers > 0:
        return df
    
    # Créer une nouvelle ligne avec le label
    new_row = pd.DataFrame([[missing_label] * df.shape[1]], columns=df.columns)
    
    # Concaténer la nouvelle ligne avec le DataFrame d'origine
    df = pd.concat([new_row, df], ignore_index=True)
    
    # Réindexer les colonnes (facultatif si les colonnes doivent rester numérotées)
    df.columns = range(df.shape[1])
    
    return df


def find_total_indexes(series):
    """
    Renvoie la position des valeurs contenant le mot "total" (insensible à la casse)
    d'une pd.Series

    args:
        series (pd.Series)
    return
        Boolean
    """

    # uplet de True / False
    mask = series.str.contains('total', case=False, na=False)
    
    return [series.index.get_loc(idx) for idx in series[mask].index]


def remove_totals(df):
    """
    Enlève les lignes et colonnes de type "Total" de la df

    args:
        df (DataFrame)
        structure (dict)
    return:
        dict
    """
    structure = detect_structure(df)

    all_total_col_indexes = []
    for header_index in structure["headers"]:
        header = df.iloc[header_index, :]
        total_col_indexes = find_total_indexes(header)
        for index in total_col_indexes:
            if index not in all_total_col_indexes:
                all_total_col_indexes.append(index)
    
    all_total_row_indexes = []
    for variable_index in structure["variables"]:
        variable = df.iloc[:, variable_index]
        total_row_indexes = find_total_indexes(variable)

        for index in total_row_indexes:
            if index not in all_total_row_indexes:
                all_total_row_indexes.append(index)
                
    df = df.drop(columns=df.columns[all_total_col_indexes])
    df = df.drop(index=all_total_row_indexes)

    df.columns = range(df.shape[1])
    df.reset_index(drop=True, inplace=True)

    return df

def split_df(df):
    """
    Divise la DataFrame en plusieurs sous-DataFrames en fonction des headers et des variables trouvées
    
    args:
        df (pd.DataFrame): le DataFrame d'origine
        structure (dict):
            "headers": liste des index des headers
            "variables": liste des index des variables
    
    Returns:
        list: liste des sous-DataFrames découpés
    """
    structure = detect_structure(df)
    splitted_dfs = []
    
    # Obtenir les index des headers (lignes) et des variables (colonnes)
    header_indexes = structure["headers"]
    variable_indexes = structure["variables"]

    # Identifier les intervalles pour les headers
    header_intervals = []
    if header_indexes:  # Vérifier qu'il y a au moins un header
        current_start = header_indexes[0]  # Initialiser au premier header
        for i in range(len(header_indexes) - 1):
            if header_indexes[i + 1] > header_indexes[i] + 1:  # Gap détecté
                header_intervals.append((current_start, header_indexes[i] + 1))
                current_start = header_indexes[i + 1]  # Début du prochain intervalle
        # Ajouter le dernier intervalle
        header_intervals.append((current_start, None))

    # Identifier les intervalles pour les variables
    variable_intervals = []
    if variable_indexes:  # Vérifier qu'il y a au moins une variable
        current_start = variable_indexes[0]  # Initialiser à la première variable
        for i in range(len(variable_indexes) - 1):
            if variable_indexes[i + 1] > variable_indexes[i] + 1:  # Gap détecté
                variable_intervals.append((current_start, variable_indexes[i] + 1))
                current_start = variable_indexes[i + 1]  # Début du prochain intervalle
        # Ajouter le dernier intervalle
        variable_intervals.append((current_start, None))

    # Découper la DataFrame en fonction des intervalles
    for h_start, h_end in header_intervals:
        for v_start, v_end in variable_intervals:
            # Si h_end ou v_end est None, cela signifie "jusqu'à la fin"
            sub_df = df.iloc[
                h_start:(h_end if h_end is not None else None),  # Lignes
                v_start:(v_end if v_end is not None else None)   # Colonnes
            ]
            # Réindexer le sous-DataFrame
            sub_df = sub_df.reset_index(drop=True)  # Réinitialiser l'index des lignes
            sub_df.columns = range(sub_df.shape[1])  # Réinitialiser les colonnes
            splitted_dfs.append(sub_df)

    return splitted_dfs


def fill_col_names(df, missing_label):
    structure = detect_structure(df)

    nb_headers = len(structure["headers"])
    variable_indexes = structure["variables"]
    variables = df.iloc[:, variable_indexes]

    previous_col_names = None
    for col_index, col in variables.T.iterrows():
        col_names = col[:nb_headers].unique()
        col_name = col_names[-1]

        if np.array_equal(col_names, previous_col_names):
            col_name = missing_label
        
        df.iloc[:nb_headers, col_index] = col_name
        previous_col_names = col_names
    
    return df


def fill_headers(df, missing_label="unknown"):
    """
    Remplit les valeurs manquantes des lignes spécifiées par `header_indexes`
    et remplace les valeurs restantes par "unknown".
    
    Args:
        df (pd.DataFrame): Le DataFrame à traiter.
    
    Returns:
        pd.DataFrame: Le DataFrame avec les headers remplis.
    """
    # Détection de la structure pour obtenir les lignes des headers
    structure = detect_structure(df)
    header_indexes = structure["headers"]

    df.iloc[header_indexes, :] = df.iloc[header_indexes, :].replace("", None)

    df.iloc[header_indexes, :] = (
        df.iloc[header_indexes, :]
        .ffill(axis=1)             # Remplissage horizontal (forward fill)
        .fillna(missing_label)    # Remplissage final avec le label
    )

    return df


# Fonction fictive pour détecter les headers
def fill_variables(df):
    """
    Remplit les colonnes de variables vers le bas (forward fill).
    Si une seule colonne est présente, elle est également remplie.
    
    Args:
        df (pd.DataFrame): Le DataFrame à traiter.
    
    Returns:
        pd.DataFrame: Le DataFrame avec les variables remplies.
    """
    structure = detect_structure(df)
    variable_indexes = structure["variables"]

    # Vérifier s'il y a des variables à remplir
    if not variable_indexes:
        return df

    variables = df.iloc[:, variable_indexes]

    # Si une seule colonne (Series), remplir directement
    if isinstance(variables, pd.Series) or variables.shape[1] == 1:
        df.iloc[:, variable_indexes] = df.iloc[:, variable_indexes].replace("", None)
        df.iloc[:, variable_indexes] = variables.fillna(method="ffill")
        return df

    # Remplir toutes les colonnes sauf la dernière
    variables.iloc[:, :-1].replace("", None)
    variables.iloc[:, :-1] = variables.iloc[:, :-1].fillna(method="ffill")
    df.iloc[:, variable_indexes] = variables

    return df


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



def unpivot_df(df, value_colname, missing_label):
    """
    Transforme un DataFrame avec plusieurs en-têtes en un DataFrame au format "tidy".
    
    :param df: DataFrame brut à transformer.
    :param nb_headers: Nombre de lignes d'en-tête à utiliser pour le MultiIndex.
    :return: DataFrame au format "tidy".
    """
    structure = detect_structure(df)
    nb_headers = len(structure["headers"])
    nb_variables = len(structure["variables"])
    nb_values = df.shape[1] - nb_variables
  
    headers = df.iloc[:nb_headers]

    # Crée le MultiIndex (en-têtes)
    df.columns = pd.MultiIndex.from_frame(headers.T)
    df.columns = clean_multi_index(df.columns)

    # Réinitialise l'index
    df = df.iloc[nb_headers:].reset_index(drop=True)

    variables_cols = df.columns.tolist()[:nb_variables]
    values_cols = df.columns.tolist()[nb_variables:]

    # Dépivote toutes les colonnes sauf celles considérées comme des variables
    print(values_cols)
    df_unpivot = df.melt(id_vars=variables_cols, value_vars=values_cols, var_name=missing_label, value_name=value_colname)
    print(df_unpivot)

    return df_unpivot

def simplify_columns(columns):
    """
    Transforme les noms de colonnes en une version simplifiée :
    - Si le nom est un tuple (MultiIndex), conserve uniquement le premier élément.
    - Si le nom est une chaîne simple, le conserve tel quel.

    Args:
        columns (pd.Index or list): Liste des noms de colonnes.

    Returns:
        list: Liste des noms de colonnes simplifiés.
    """
    simplified = []
    for col in columns:
        if isinstance(col, tuple):  # Si la colonne est un tuple (MultiIndex)
            simplified.append(col[0])  # Conserve uniquement le premier élément
        else:
            simplified.append(col)  # Garde la colonne telle quelle si simple
    return simplified

def preprocess(df, missing_label):
    df = format_df(df)
    df = add_header(df, missing_label)

    df = fill_headers(df, missing_label)
    df = fill_variables(df)
    df = remove_totals(df)

    df_splitted = split_df(df)
    df_splitted = [fill_col_names(df, missing_label) for df in df_splitted]

    return df_splitted


def app(raw_df_list, missing_label="unknown", meta_data="à voir"):
    """
    Traite une liste de DataFrames bruts en effectuant des étapes de prétraitement,
    de détection de structure et de réorganisation des données.

    Args:
        raw_df_list (list): Liste des DataFrames bruts à traiter.
        meta_data (dict): Métadonnées associées aux DataFrames.

    Returns:
        dict: Structure contenant les DataFrames bruts et leurs versions traitées.
    """
    processed_data = {}

    for idx, raw_df in enumerate(raw_df_list):  # Commencer à indexer à 1
        # Étape de prétraitement
        df_splitted = preprocess(raw_df, missing_label)

        processed_dfs = []
        for df in df_splitted:
            # Détection de la structure
            structure = detect_structure(df)

            # Transformation du DataFrame
            df_unpivot = unpivot_df(df, value_colname="valeur", missing_label=missing_label)
            df_unpivot.columns = simplify_columns(df_unpivot.columns)
            processed_dfs.append(df_unpivot)

        processed_data[idx] = {
            "raw_df": raw_df,
            "processed_df": processed_dfs
            # "meta_data": meta_data[idx]
        }

    return processed_data



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
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
print("\n \n \n aaaaaaaaaaaaaaaaaaaaaaaaaaaa")
processed_data = app(dataframes)
show_processed_dataframes(processed_data)

# show_dataframes(dataframes, dfs)
# print(df)

# il faut remplir avant car total doit se remplir

# ensuite split puis enlever total ou inverse

# étapes
# formate simple
# trouver les headers/variables => structure
# fill les headers/variables
# enlever les totals
# re structure (éviter de relancer la fonction, il faudrait calculer la nouvelle structure en fonction des lignes/cols enlevées)
# split la dataframe en plusieurs si les headers/variables sont éloignés
# re structure chaque df (pareil pas relancer)

# pour chaque variable regarder au dessus (index pas supérieur au nb de headers), savoir si titre du tableau ou nom de la colonne.
# traiter si plusieurs mots trouvés (si plusieurs headers)

# si variable suivante mêmes noms => changer

# Si titre mettre dans une colonne
# Sinon, nom de la variable