import pdfplumber
import pandas as pd

settings = {"vertical_strategy":"text", "intersection_tolerance": 40}

with pdfplumber.open(r"data\bilans_sociaux\CNP-Assurances-Bilan-social-2023.pdf") as pdf:
    page = pdf.pages[17]
    ph, pw, ratio = page.height, page.width, .1
    page = page.crop((ratiopw, ratioph, (1-ratio)pw, (1-ratio)ph))
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