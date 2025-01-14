import pandas as pd
import sys
import re
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

sys.path.append("get_tables_PDF/utils")
from dataframe_viewer import show_dataframes
from processed_dataframe_viewer import show_processed_dataframes


"""
format_df(df)
has_numerical_values(series)
has_year_sequency(series, series_index, min_year=2020, max_year=2025)
is_value(series, series_index)
detect_structure(df)
add_header(df, missing_label="unknown")
remove_totals(df)


fill_variable_names(df, missing_label)
fill_headers(df, missing_label="unknown")
fill_variables(df)
split_df(df)
clean_multi_index(multi_index)
unpivot_df(df, value_colname, missing_label)
format_colnames(columns)
preprocess(df, missing_label)
process_tables(raw_df_list, missing_label="unknown")
"""

def format_df(df):
    """
    Formate la DataFrame en supprimant les lignes et colonnes vides, 
    convertissant toutes les valeurs et colonnes en chaînes de caractères
    
    args: 
        df (DataFrame): df à formater

    return:
        DataFrame: df formatée
    """

    df = df.dropna(how='all', axis=0)
    df = df.dropna(how='all', axis=1)
    df = df.map(lambda x: str(x) if pd.notnull(x) else "")
    return df

def has_numerical_values(series):
    """
    Renvoie True si la ligne possède une ou plusieurs valeurs dites numériques

    args:
        series (pd.Series)
    return:
        Boolean
    """
    # Contient des chiffres, points, virgules, devises
    pattern = r"^[\d.,%€$£₹]*$"

    for value in series:
        if bool(re.match(pattern, value)):
            return True
        
    return False

def has_year_sequency(series, series_index, min_year=2020, max_year=2025):
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
        return series_index == 0 and min_year <= int_values[0] <= max_year

    # Vérifie si toutes les valeurs sont dans la plage d'année
    return all(min_year <= num <= max_year for num in int_values)

def detect_structure(df):
    """
    Renvoie la structure de la df en précisant:
    où se trouvent les headers (en-têtes) et les variables via leur index

    args:
        df (pd.DataFrame)
    return
        dict
    """

    # Pour chaque row, regarde si c'est un header
    header_indexes = []
    for row_index, row in df.iterrows():
        isValue = has_numerical_values(row) and not(has_year_sequency(row, row_index))
        if not isValue:
            header_indexes.append(row_index)
    
    # Pour chaque colonne, regarde si c'est une colonne
    variable_indexes = []
    for col_index in range(df.shape[1]):
        column = df.iloc[:, col_index]
        isValue = has_numerical_values(column) and not(has_year_sequency(column, col_index))
        if not isValue:
            variable_indexes.append(col_index)
    
    structure = {
        "headers": header_indexes,
        "variables": variable_indexes
    }

    return structure

def add_header(df, missing_label):
    """
    Ajoute une ligne tout en haut du DataFrame avec le label spécifié
    
    args:
        df (pd.DataFrame): Le DataFrame d'origine.
        label (str): Le label à remplir dans la ligne ajoutée.
    returns:
        pd.DataFrame: Le DataFrame modifié.
    """

    structure = detect_structure(df)
    nb_headers = len(structure["headers"])
    if nb_headers > 0:
        return df    
    
    # Créer une nouvelle ligne avec le label
    new_row = pd.DataFrame([[missing_label] * df.shape[1]], columns=df.columns)
    df = pd.concat([new_row, df], ignore_index=True)
    
    # Réindexation
    df.columns = range(df.shape[1])
    
    return df

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
        mask_total = header.str.contains('total', case=False, na=False)
        total_col_indexes = [header.index.get_loc(idx) for idx in header[mask_total].index]

        for index in total_col_indexes:
            if index not in all_total_col_indexes:
                all_total_col_indexes.append(index)
    
    all_total_row_indexes = []
    for variable_index in structure["variables"]:
        variable = df.iloc[:, variable_index]
        mask_total = variable.str.contains('total', case=False, na=False)
        total_row_indexes = [variable.index.get_loc(idx) for idx in variable[mask_total].index]

        for index in total_row_indexes:
            if index not in all_total_row_indexes:
                all_total_row_indexes.append(index)
                
    df = df.drop(columns=df.columns[all_total_col_indexes])
    df = df.drop(index=all_total_row_indexes)

    df.columns = range(df.shape[1])
    df.reset_index(drop=True, inplace=True)

    return df

def fill_variable_names(df, missing_label):
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

def fill_headers(df, missing_label):
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
    Dépivote les colonnes qui ne sont pas des variables d'une DataFrame
    
    args:
        df: DataFrame à dépivoter
        value_colname: nom de la colonne 'valeur' générée
        missing_label: nom des colonnes dépivotées

    return: DataFrame dépivotée
    """
    structure = detect_structure(df)
    nb_headers = len(structure["headers"])
    nb_variables = len(structure["variables"])
  
    headers = df.iloc[:nb_headers]

    # Crée le MultiIndex (en-têtes)
    df.columns = pd.MultiIndex.from_frame(headers.T)
    df.columns = clean_multi_index(df.columns)

    # Réinitialise l'index
    df = df.iloc[nb_headers:].reset_index(drop=True)

    # Récupérer les colonnes variables
    variables_cols = df.columns.tolist()[:nb_variables]

    # Dépivote toutes les colonnes considérées comme des variables
    df_unpivot = df.melt(id_vars=variables_cols, var_name=missing_label, value_name=value_colname)

    return df_unpivot

def format_colnames(columns):
    """
    Formate les noms de colonnes après pivot :
    - Si le nom est un tuple (MultiIndex), conserve uniquement le premier élément
    - Si le nom est une chaîne simple, le conserve tel quel

    Args:
        columns (pd.Index or list): Liste des noms de colonnes.

    Returns:
        list: Liste des noms de colonnes formatés
    """
    simplified = []
    for col in columns:
        if isinstance(col, tuple):  # Si la colonne est un tuple (MultiIndex)
            simplified.append(col[0])  # Conserve uniquement le premier élément
        else:
            simplified.append(col)  # Garde la colonne telle quelle si simple
    return simplified

def process_tables(df_list, missing_label="unknown"):
    """
    Dépivote toutes les df qui sont dans une liste

    args:
        raw_df_list (list): Liste des DataFrames bruts à traiter.
        meta_data (dict): Métadonnées associées aux DataFrames.

    Returns:
        dict: Structure contenant les DataFrames bruts et leurs versions traitées.
    """

    processed_dfs = []
    for idx, df in enumerate(df_list):
        df = format_df(df)
        df = add_header(df, missing_label)

        df = fill_headers(df, missing_label)
        df = fill_variables(df)
        df = remove_totals(df)

        # Dépivote chaque df
        df_unpivot = unpivot_df(df, value_colname="valeur", missing_label=missing_label)
        df_unpivot.columns = format_colnames(df_unpivot.columns)
        processed_dfs.append(df_unpivot)

    return processed_dfs