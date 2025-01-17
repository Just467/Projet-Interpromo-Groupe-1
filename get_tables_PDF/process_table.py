import pandas as pd
import sys
import re
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

sys.path.append("get_tables_PDF/utils")
from utils.dataframe_viewer import show_dataframes
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

def detect_structure(df, header_list):
    """
    Renvoie la structure de la df en précisant:
    où se trouvent les headers (en-têtes) et les variables via leur index

    args:
        df (pd.DataFrame)
    return
        dict
    """

    header_indexes = []
    for row_index, row in enumerate(header_list):
        if row[0] == 'header':
            header_indexes.append(row_index)

    # Pour chaque colonne, regarde si c'est une colonne
    numeric_pattern=r'^[\d.,\s€$£¥%]*(?: *ans)?$'
    year_pattern=r'^20[0-2]\d$'
    variable_indexes = []
    for col_index in range(df.shape[1]):
        column = df.iloc[:, col_index]
        isVariable = True
        for cell in column:
            if isinstance(cell, str) and cell.strip() == "":
                continue

            if re.match(numeric_pattern, cell) and not re.match(year_pattern, cell):
                    isVariable = False
                    break
            
        if isVariable:
            variable_indexes.append(col_index)

    structure = {
        "headers": header_indexes,
        "variables": variable_indexes
    }

    return structure


def add_header(df, header_list, missing_label):
    """
    Ajoute une ligne tout en haut du DataFrame avec le label spécifié
    
    args:
        df (pd.DataFrame): Le DataFrame d'origine.
        label (str): Le label à remplir dans la ligne ajoutée.
    returns:
        pd.DataFrame: Le DataFrame modifié.
    """

    structure = detect_structure(df, header_list)
    nb_headers = len(structure["headers"])

    if nb_headers > 0:
        return df    
    
    # Créer une nouvelle ligne avec le label
    new_row = pd.DataFrame([[missing_label] * df.shape[1]], columns=df.columns)
    df = pd.concat([new_row, df], ignore_index=True)
    df.columns = range(df.shape[1])
    
    return df


def remove_totals(df, header_list):
    """
    Enlève les lignes et colonnes de type "Total" de la df

    args:
        df (DataFrame)
        structure (dict)
    return:
        dict
    """
    structure = detect_structure(df, header_list)
    
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


def fill_variable_names(df, header_list, missing_label):
    structure = detect_structure(df, header_list)

    nb_headers = len(structure["headers"])
    variable_indexes = structure["variables"]
    variables = df.iloc[:, variable_indexes]

    previous_col_names = None
    for col_index, col in variables.T.iterrows():
        col_names = col[:nb_headers].unique()

        # Vérifiez si col_names est vide
        if len(col_names) == 0:
            df.iloc[:nb_headers, col_index] = missing_label

        if previous_col_names is not None and np.array_equal(col_names, previous_col_names):
            df.iloc[:nb_headers, col_index] = missing_label
        
        previous_col_names = col_names
    return df


def fill_headers(df, header_list, missing_label):
    """
    Remplit les valeurs manquantes des lignes spécifiées par `header_indexes`
    et remplace les valeurs restantes par "unknown".
    
    Args:
        df (pd.DataFrame): Le DataFrame à traiter.
    
    Returns:
        pd.DataFrame: Le DataFrame avec les headers remplis.
    """

    # Détection de la structure pour obtenir les lignes des headers
    structure = detect_structure(df, header_list)
    header_indexes = structure["headers"]

    df.iloc[header_indexes, :] = df.iloc[header_indexes, :].replace("", None)

    df.iloc[header_indexes, :] = (
        df.iloc[header_indexes, :]
        .ffill(axis=1)             # Remplissage horizontal (forward fill)
        .fillna(missing_label)    # Remplissage final avec le label
    )

    return df


def fill_variables(df, header_list):
    """
    Remplit les colonnes de variables vers le bas (forward fill).
    Si une seule colonne est présente, elle est également remplie.
    
    Args:
        df (pd.DataFrame): Le DataFrame à traiter.
    
    Returns:
        pd.DataFrame: Le DataFrame avec les variables remplies.
    """
    structure = detect_structure(df, header_list)
    variable_indexes = structure["variables"]

    # Vérifier s'il y a des variables à remplir
    if not variable_indexes:
        return df

    variables = df.iloc[:, variable_indexes].replace("", None)

    df.iloc[:, variable_indexes] = variables.fillna(method="ffill")

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
        # Détermine le nom de base (dernier élément pour MultiIndex)
        primary_name = colname[-1] if isinstance(colname, tuple) else colname

        # Vérifie si primary_name est None
        if primary_name is None:
            primary_name = missing_label

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


def unpivot_df(df, header_list, current_year="2023", year_colname="Année", value_colname="Valeur", unit_colname="Unité", default_unit="nombre", missing_label="unknown"):
    """
    Dépivote les colonnes d'une df cleaned
    
    args:
        df: DataFrame à dépivoter
        value_colname: nom de la colonne 'valeur' générée
        missing_label: nom des colonnes dépivotées

    return: DataFrame dépivotée
    """
    structure = detect_structure(df, header_list)
    nb_headers = len(structure["headers"])
    nb_variables = len(structure["variables"])
    headers = df.iloc[:nb_headers]

    year_pattern = r'^20[0-2]\d$'
    has_year_corner = False
    if nb_headers > 0:
        top_left_corner = df.iloc[nb_headers-1, 0]
        if re.match(year_pattern, top_left_corner):
            df.iloc[:nb_headers, 0] = ""
            has_year_corner = True

    # Crée le MultiIndex (en-têtes)
    df = add_header(df, header_list, missing_label)
    df.columns = pd.MultiIndex.from_frame(headers.T)
    df.columns = clean_multi_index(df.columns)

    # Réinitialise l'index
    df = df.iloc[nb_headers:].reset_index(drop=True)

    # Récupérer les colonnes variables
    variables_cols = df.columns.tolist()[:nb_variables]

    # Dépivote toutes les colonnes considérées comme des variables
    df_unpivot = df.melt(id_vars=variables_cols, value_name=value_colname)

    # Concaténation des valeurs pour les colonnes sans nom
    df_unpivot.columns = format_colnames(df_unpivot)

    # Ajout de la colonne "unit"
    df_unpivot = add_unit_column(df_unpivot, value_colname, unit_colname, default_unit)

    # Ajout de la colonne "Année"
    if has_year_corner:
        df_unpivot[year_colname] = top_left_corner
    else:
        df_unpivot[year_colname] = current_year

    return df_unpivot


def detect_bad_df(df, header_list):
    if df.shape[0] < 2 or df.shape[1] < 2:
        return True
    if len([header_type for header_type, header_top in header_list if not header_type]) == 0:
        return True
    return False


def split_dataframe(df:pd.core.frame.DataFrame, header_list:list)->list:
    """Split a dataframes with a list of indexes to split. Does not split when value of indexes are consecutives.

    Args:
        df (pd.core.frame.DataFrame): a dataframe
        indexes (list): a list of integers

    Returns:
        list: a list of dataframes
    """
    indexes = [(i, top) for i, (header, top) in enumerate(header_list) if header]
    splitted_df_list = []
    if indexes:
        previous_index = indexes[0][0]
        previous_top = indexes[0][1]
        for index_pos, (index, top) in enumerate(indexes[1:], start=1):
                if index != indexes[index_pos-1][0] + 1:
                        splitted_df_list.append( (df.iloc[previous_index:index].reset_index(drop=True),
                                                  previous_top,
                                                  header_list[previous_index:index]) )
                        previous_index = index
                        previous_top = top
        splitted_df_list.append((df.iloc[previous_index:].reset_index(drop=True),
                                 previous_top,
                                 header_list[previous_index:]))
        return splitted_df_list
    else:
        return [(df, 0, header_list)]


def clean_df(df, header_list,
             missing_label="unknown"):
    """
    Applique un nettoyage puis détecte s'il y a plusieurs dfs et les split
    permettant de dépivoter la df correctement
    """
    # Splitting
    index_none_row = [i for i, (header, top) in enumerate(header_list) if header=='none']
    header_list = [(header, top) for header, top in header_list if header!='none']
    df = df.drop(index_none_row)
    splitted_df_list = split_dataframe(df, header_list)

    # Formatting
    final_df_list = []
    # for df, top, header_list in df_list:
    for df, top, header_list in splitted_df_list:
        df = df.dropna(how="all")
        df = df.dropna(axis=1, how="all")
        df = df.fillna("").astype(str)
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        df = fill_headers(df, header_list, missing_label)
        df = fill_variable_names(df, header_list, missing_label)
        df = fill_variables(df, header_list)
        bad_df = detect_bad_df(df, header_list)
        if not bad_df:
            final_df_list.append((df, top, header_list))
    return final_df_list