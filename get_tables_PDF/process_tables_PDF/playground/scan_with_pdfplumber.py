import pdfplumber
import pandas as pd

settings = {"vertical_strategy":"text", "text_y_tolerance": 1000000, "join_x_tolerance": 100000}

with pdfplumber.open(r"data\bilans_sociaux\CNP-Assurances-Bilan-social-2023.pdf") as pdf:
    page = pdf.pages[5]
    table = pd.DataFrame(page.extract_table(settings))

page.to_image().debug_tablefinder(settings).show()

def clean_table_pdfplumber(df):
    row_to_drop = []
    for index, row in df.iterrows():
        if not any(row[1:]):
            row_to_drop.append(index)
    df = df.drop(row_to_drop, axis=0)

    return df

table = clean_table_pdfplumber(table)
print(table)
