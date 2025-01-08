import pdfplumber

def find_pages_with_tables(pdf_path, settings=None):
    """
    Retourne la des pages contenant un tableau dans un fichier PDF.
    
    args:
        pdf_path (str): Chemin vers le fichier PDF.
        settings (dict): Paramètres pour `extract_table`. Par défaut, None.
    
    return:
        list: Liste des numéros de pages contenant au moins un tableau.
    """
    pages_with_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables(settings) if settings else page.extract_tables()
            
            if tables and any(tables):
                pages_with_tables.append(page_number)

    return pages_with_tables


def fill_df():
    