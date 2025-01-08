import pdfplumber
import pandas as pd
import sys
sys.path.append('get_tables_PDF/utils')

from table_viewer import show_table
from image_viewer import show_images_with_tables

value_range = [0, 1, 2, 3, 5, 10, 15, 25, 50]

# Générer toutes les combinaisons possibles


images_with_settings = []

for settings in list_settings :
    with pdfplumber.open(r"data\bilans_sociaux\CNP-Assurances-Bilan-social-2023.pdf") as pdf:
        page = pdf.pages[5]
        ph, pw, ratio = page.height, page.width, .1
        page = page.crop((ratio*pw, ratio*ph, (1-ratio)*pw, (1-ratio)*ph))
        
        tables = page.extract_tables(settings)
        if(tables):
            df = pd.DataFrame(tables[0])
            df.columns = df.columns.astype(str)


            image = page.to_image().debug_tablefinder(settings)
            images_with_settings.append({"image": image, "settings": settings, "dataframe": df})

show_images_with_tables(images_with_settings)