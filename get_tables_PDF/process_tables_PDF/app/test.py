import pandas as pd

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


# Générer une DataFrame d'exemple
def generate_example_df():
    data = {
        " Colonne 1 ": ["  Valeur 1  ", None, "  Valeur 3  "],
        "Colonne 2": [None, None, None],
        " Colonne 3 ": ["   ", "  Valeur 4  ", "  Valeur 5 "]
    }
    df = pd.DataFrame(data)
    return df

# Exemple d'utilisation
example_df = generate_example_df()
print("Avant formatage :")
print(example_df)

formatted_df = format_df(example_df)
print("\nAprès formatage :")
print(formatted_df)
