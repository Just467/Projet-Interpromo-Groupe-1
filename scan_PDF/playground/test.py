import pdfplumber
import pandas as pd
from tkinter import Tk, Label, Button, filedialog, Frame
from tkinter.ttk import Treeview, Scrollbar

class PDFTableViewer:
    def __init__(self, master, pdf_file):
        self.master = master
        self.master.title("PDF Table Viewer")

        self.pdf_file = pdf_file
        self.tables = []
        self.current_index = 0

        # Cadre principal
        self.main_frame = Frame(master)
        self.main_frame.pack(fill="both", expand=True)

        # Treeview pour afficher les tables
        self.tree = Treeview(self.main_frame, show="headings")
        self.tree.pack(side="top", fill="both", expand=True)

        # Scrollbars pour le Treeview
        self.scroll_x = Scrollbar(self.main_frame, orient="horizontal", command=self.tree.xview)
        self.scroll_x.pack(side="bottom", fill="x")
        self.scroll_y = Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.scroll_y.pack(side="right", fill="y")

        self.tree.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)

        # Boutons de navigation
        self.button_frame = Frame(master)
        self.button_frame.pack()
        self.prev_button = Button(self.button_frame, text="<< Previous", command=self.prev_table)
        self.prev_button.pack(side="left", padx=10, pady=10)
        self.next_button = Button(self.button_frame, text="Next >>", command=self.next_table)
        self.next_button.pack(side="right", padx=10, pady=10)

        # Charger les tables depuis le PDF
        self.load_pdf_tables()

    def load_pdf_tables(self):
        with pdfplumber.open(self.pdf_file) as pdf:
            for page_number, page in enumerate(pdf.pages):
                print(f"Processing page {page_number + 1}...")
                # Extraire les tables de la page
                tables = page.extract_tables()
                if tables:
                    for table_index, table in enumerate(tables):
                        # Convertir la table en DataFrame
                        df = pd.DataFrame(table)
                        self.tables.append({
                            "df": df,
                            "page": page_number + 1,
                            "table_index": table_index + 1
                        })

        if self.tables:
            self.display_table(self.current_index)
        else:
            print("No tables found in the document.")
            self.master.title("No tables found")

    def display_table(self, index):
        # Effacer les données actuelles du Treeview
        for column in self.tree.get_children():
            self.tree.delete(column)
        self.tree["columns"] = []

        table_info = self.tables[index]
        df = table_info["df"]
        page_number = table_info["page"]
        table_index = table_info["table_index"]

        # Configurer les colonnes
        if not df.empty:
            self.tree["columns"] = list(range(len(df.columns)))  # Utiliser des index pour les colonnes
            for col_index, col_name in enumerate(df.iloc[0]):  # Utiliser la première ligne comme en-tête
                self.tree.heading(col_index, text=col_name)
                # Ajuster automatiquement la largeur des colonnes
                max_width = max(len(str(value)) for value in df[col_index].fillna("").astype(str))
                self.tree.column(col_index, width=max(150, max_width * 10), anchor="center")

            # Insérer les lignes dans le Treeview
            for _, row in df.iterrows():
                self.tree.insert("", "end", values=list(row))

        # Mettre à jour le titre de la fenêtre
        self.master.title(f"Table {table_index} on Page {page_number}")

    def prev_table(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.display_table(self.current_index)

    def next_table(self):
        if self.current_index < len(self.tables) - 1:
            self.current_index += 1
            self.display_table(self.current_index)


# Fonction principale
def main():
    # Boîte de dialogue pour sélectionner un fichier PDF
    pdf_file = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF Files", "*.pdf")])

    if not pdf_file:
        print("No file selected.")
        return

    # Lancer l'interface Tkinter
    root = Tk()
    root.geometry("800x600")
    app = PDFTableViewer(root, pdf_file)
    root.mainloop()


if __name__ == "__main__":
    main()
