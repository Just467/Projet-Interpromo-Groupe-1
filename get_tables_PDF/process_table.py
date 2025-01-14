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
    pattern = r"^[\d.,%€$£\s]*$"

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

        # Vérifiez si col_names est vide
        if len(col_names) == 0:
            col_name = missing_label  # Si vide, utilisez une valeur par défaut
        else:
            col_name = col_names[-1]

        if previous_col_names is not None and np.array_equal(col_names, previous_col_names):
            col_name = missing_label  # Si les noms sont identiques, utilisez missing_label
        
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


def format_colnames(df, missing_label="unknown"):
    """
    Formate les noms de colonnes après pivot :
    - Si une colonne contient "unknown" dans son nom, remplace le nom par une concaténation des valeurs uniques de la colonne
    - Sinon, garde le nom tel quel

    args:
        df (pd.DataFrame): DataFrame à formater.

    returns:
        list: Liste des noms de colonnes formatés
    """
    simplified = []
    for colname in df.columns:
        # Détermine le nom de base (premier élément pour MultiIndex)
        primary_name = colname[0] if isinstance(colname, tuple) else colname

        if missing_label in primary_name:
            unique_values = df[colname].dropna().unique()
            if len(unique_values) > 0:
                # Concatène les valeurs
                new_name = ", ".join(map(str, unique_values))
            else:
                new_name = missing_label
            simplified.append(new_name)
        else:
            simplified.append(primary_name)

    return simplified

def add_unit_column(df, value_colname="value", unit_colname="unit", default_unit="nombre"):
    """
    Ajoute une colonne 'unit' à la df en analysant la colonne 'value'

    args:
        df (pd.DataFrame): DataFrame contenant une colonne 'value' en type str.

    returns:
        pd.DataFrame: DataFrame avec les colonnes nettoyées 'value' et 'unit'.
    """
    def clean_value_unit(value):
        value = value.replace(" ", "")

        # Extraire les chiffres avec la virgule (convertie en point)
        number_match = re.search(r"[\d,]+", value)
        number = number_match.group(0).replace(",", ".") if number_match else None

        # Extraire les symboles non numériques
        unit = re.sub(r"[\d.,]+", "", value)

        # Si aucune unité trouvée, mettre "nombre" par défaut
        unit = unit if unit else default_unit

        return float(number) if number else None, unit

    # Appliquer la transformation à la colonne 'value'
    df[value_colname], df[unit_colname] = zip(*df[value_colname].map(clean_value_unit))

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


def clean_df(df, missing_label="unknown"):
    """
    Applique un nettoyage puis détecte s'il y a plusieurs dfs et les split
    permettant de dépivoter la df correctement
    """
    df = format_df(df)
    df = fill_headers(df, missing_label)
    df = fill_variables(df)
    df = remove_totals(df)

    df_splitted = split_df(df)
    df_splitted = [fill_variable_names(df, missing_label) for df in df_splitted]

    return df_splitted


def unpivot_df(df, value_colname="value", unit_colname="unit", default_unit="nombre", missing_label="unknown"):
    """
    Dépivote les colonnes d'une df cleaned
    
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
    df = add_header(df, missing_label)
    df.columns = pd.MultiIndex.from_frame(headers.T)
    df.columns = clean_multi_index(df.columns)

    # Réinitialise l'index
    df = df.iloc[nb_headers:].reset_index(drop=True)

    # Récupérer les colonnes variables
    variables_cols = df.columns.tolist()[:nb_variables]

    # Dépivote toutes les colonnes considérées comme des variables
    df_unpivot = df.melt(id_vars=variables_cols, var_name=missing_label, value_name=value_colname)

    # Concaténation des valeurs pour les colonnes sans nom
    df_unpivot.columns = format_colnames(df_unpivot)

    # Ajout de la colonne "unit"
    df_unpivot = add_unit_column(df_unpivot, value_colname, unit_colname, default_unit)
    return df_unpivot

# data1 = [
#     [None, None, "Homme", None, "Femme", None],
#     [None, "categ", "Fonctionnaire", "Non Fonctionnaire", "Fonctionnaire", "Non Fonctionnaire"],
#     [2021, "Catégorie A", "8 €", 9, 10, 11],
#     [2021, "Catégorie B", 15, 25, 20, 30],
#     [2021, "Catégorie C", 45, 35, 40, 25],
#     [2022, "Catégorie A", 50, 55, 60, 65],
#     [2022, "Catégorie B", 70, 75, 80, 85]
# ]

# df = pd.DataFrame(data1)

# cleaned_df = clean_df(df)
# print(cleaned_df)
# # print(unpivot_df(cleaned_df))