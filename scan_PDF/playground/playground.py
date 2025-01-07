import pdfplumber
import pandas as pd
from tkinter import Tk, Label, Button, filedialog
from PIL import Image, ImageTk

class PDFTableViewer:
    def __init__(self, master, pdf_file):
        self.master = master
        self.master.title("PDF Table Viewer")

        self.pdf_file = pdf_file
        self.tables = []
        self.current_index = 0

        # Configure la fenêtre pour qu'elle soit redimensionnable
        self.master.geometry("800x600")
        self.master.resizable(True, True)

        # Frame principale pour l'image et les boutons
        self.main_frame = Label(master)
        self.main_frame.pack(fill='both', expand=True)

        # Label pour afficher l'image
        self.label = Label(self.main_frame)
        self.label.pack(fill='both', expand=True)

        # Frame pour les boutons (centrés sous l'image)
        self.button_frame = Label(self.main_frame)
        self.button_frame.pack()

        # Bouton précédent
        self.prev_button = Button(self.button_frame, text="<< Previous", command=self.prev_table)
        self.prev_button.pack(side="left", padx=20, pady=10)

        # Bouton suivant
        self.next_button = Button(self.button_frame, text="Next >>", command=self.next_table)
        self.next_button.pack(side="right", padx=20, pady=10)

        # Charger les tables depuis le PDF
        self.load_pdf_tables()

        # Lier l'événement de redimensionnement de la fenêtre
        self.master.bind('<Configure>', self.on_resize)

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
                        image = page.to_image().debug_tablefinder()
                        self.tables.append({
                            "df": df,
                            "image": image,
                            "page": page_number + 1,
                            "table_index": table_index + 1
                        })

        if self.tables:
            self.display_table(self.current_index)
        else:
            print("No tables found in the document.")
            self.master.title("No tables found")

    def display_table(self, index):
        self.current_table_info = self.tables[index]
        self.update_image()

        # Mettre à jour le titre de la fenêtre
        page_number = self.current_table_info["page"]
        table_index = self.current_table_info["table_index"]
        self.master.title(f"Table {table_index} on Page {page_number}")

    def update_image(self):
        # Obtenir la taille actuelle de la fenêtre
        window_width = self.master.winfo_width()
        window_height = self.master.winfo_height()

        # Calculer la hauteur disponible pour l'image (en soustrayant la hauteur des boutons)
        button_height = self.button_frame.winfo_height()
        if button_height == 0:
            button_height = 50  # Valeur par défaut si la hauteur n'est pas encore disponible

        available_height = window_height - button_height - 50  # Ajustement pour marges

        # Récupérer l'image originale
        image = self.current_table_info["image"]
        pil_image = image.annotated

        # Calculer le ratio d'aspect
        original_width, original_height = pil_image.size
        aspect_ratio = original_width / original_height

        # Redimensionner l'image pour correspondre à la hauteur disponible
        new_height = available_height
        new_width = int(new_height * aspect_ratio)

        # Si la nouvelle largeur dépasse la largeur de la fenêtre, ajuster en conséquence
        if new_width > window_width:
            new_width = window_width - 50  # Ajustement pour marges
            new_height = int(new_width / aspect_ratio)

        # Redimensionner l'image
        pil_image_resized = pil_image.resize((new_width, new_height), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(pil_image_resized)

        # Mettre à jour le label avec l'image
        self.label.config(image=tk_image)
        self.label.image = tk_image

    def on_resize(self, event):
        # Mettre à jour l'image lors du redimensionnement de la fenêtre
        self.update_image()

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
    # Lancer l'interface Tkinter
    root = Tk()

    # Boîte de dialogue pour sélectionner un fichier PDF
    pdf_file = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF Files", "*.pdf")])

    if not pdf_file:
        print("No file selected.")
        return

    app = PDFTableViewer(root, pdf_file)
    root.mainloop()


if __name__ == "__main__":
    main()
