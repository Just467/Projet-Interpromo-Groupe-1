import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QPushButton, QLineEdit, QWidget, QHBoxLayout, QLabel, QComboBox, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt


class ExcelLikeEditor(QMainWindow):
    def __init__(self, dataframe):
        super().__init__()
        self.setWindowTitle("Excel-Like DataFrame Editor")
        self.dataframe = dataframe

        # Créer le tableau
        self.table = QTableWidget()
        self.load_dataframe_into_table()

        # Boutons
        save_button = QPushButton("Save to Excel")
        save_button.clicked.connect(self.save_to_excel)

        delete_col_button = QPushButton("Delete Column")
        delete_col_button.clicked.connect(self.delete_column)

        pivot_button = QPushButton("Pivot Columns")
        pivot_button.clicked.connect(self.pivot_columns)

        change_colname_button = QPushButton("Change Column Name")
        change_colname_button.clicked.connect(self.change_column_name)

        # Sélection des colonnes pour pivoter
        self.combo_col1 = QComboBox()
        self.combo_col2 = QComboBox()
        self.new_column_name = QLineEdit()
        self.new_column_name.setPlaceholderText("Enter new column name...")

        # Layout des boutons
        button_layout = QHBoxLayout()
        button_layout.addWidget(delete_col_button)
        button_layout.addWidget(QLabel("Column 1:"))
        button_layout.addWidget(self.combo_col1)
        button_layout.addWidget(QLabel("Column 2:"))
        button_layout.addWidget(self.combo_col2)
        button_layout.addWidget(QLabel("New Column Name:"))
        button_layout.addWidget(self.new_column_name)
        button_layout.addWidget(pivot_button)
        button_layout.addWidget(change_colname_button)
        button_layout.addWidget(save_button)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        layout.addWidget(button_widget)

        # Widget principal
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Initialiser les colonnes dans les ComboBoxes
        self.update_comboboxes()

        # Écouter les touches
        self.table.setFocusPolicy(Qt.StrongFocus)
        self.table.keyPressEvent = self.handle_key_press

    def load_dataframe_into_table(self):
        """Charge les données du DataFrame dans le QTableWidget."""
        self.table.setRowCount(len(self.dataframe))
        self.table.setColumnCount(len(self.dataframe.columns))
        self.table.setHorizontalHeaderLabels(self.dataframe.columns)

        for i, row in self.dataframe.iterrows():
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

    def update_comboboxes(self):
        """Met à jour les ComboBoxes avec les noms des colonnes."""
        self.combo_col1.clear()
        self.combo_col2.clear()
        columns = list(self.dataframe.columns)
        self.combo_col1.addItems(columns)
        self.combo_col2.addItems(columns)

    def delete_column(self):
        """Supprime la colonne actuellement sélectionnée."""
        col_index = self.table.currentColumn()
        if col_index < 0:
            QMessageBox.warning(self, "Warning", "Please select a column to delete.")
            return

        col_name = self.table.horizontalHeaderItem(col_index).text()
        confirm = QMessageBox.question(
            self,
            "Delete Column",
            f"Are you sure you want to delete the column '{col_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            # Supprimer la colonne du DataFrame
            self.dataframe.drop(columns=[col_name], inplace=True)

            # Recharger le tableau
            self.load_dataframe_into_table()
            self.update_comboboxes()

    def handle_key_press(self, event):
        """Gère les pressions de touches pour la suppression des colonnes."""
        if event.key() == Qt.Key_Delete:
            self.delete_column()

    def pivot_columns(self):
        """Pivote deux colonnes sélectionnées en lignes."""
        col1 = self.combo_col1.currentText()
        col2 = self.combo_col2.currentText()
        new_column = self.new_column_name.text()

        if not col1 or not col2 or not new_column:
            QMessageBox.warning(self, "Error", "Please select columns and enter a new column name.")
            return

        # Création du DataFrame pivoté
        try:
            df_pivoted = pd.melt(
                self.dataframe,
                id_vars=[col for col in self.dataframe.columns if col not in [col1, col2]],
                value_vars=[col1, col2],
                var_name=new_column,
                value_name="Value"
            )
            self.dataframe = df_pivoted
            self.load_dataframe_into_table()
            self.update_comboboxes()
            QMessageBox.information(self, "Success", f"Columns '{col1}' and '{col2}' pivoted successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while pivoting columns: {e}")

    def change_column_name(self):
        """Change le nom d'une colonne."""
        col_index = self.table.currentColumn()
        new_name = self.new_column_name.text()
        if col_index >= 0 and new_name:
            old_name = self.table.horizontalHeaderItem(col_index).text()
            self.dataframe.rename(columns={old_name: new_name}, inplace=True)
            self.load_dataframe_into_table()
            self.update_comboboxes()
            self.new_column_name.clear()

    def save_to_excel(self):
        """Enregistre les données dans un fichier Excel."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Excel Files (*.xlsx)")
        if file_path:
            self.dataframe.to_excel(file_path, index=False)
            QMessageBox.information(self, "Success", f"File saved to {file_path}")


# Exemple d'utilisation
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Exemple de DataFrame
    import pdfplumber
    import pandas as pd

    settings = {"vertical_strategy":"text", "text_x_tolerance": 0}

    with pdfplumber.open(r"data\bilans_sociaux\CNP-Assurances-Bilan-social-2023.pdf") as pdf:
        page = pdf.pages[21]
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

    table.columns = table.columns.astype(str)
    editor = ExcelLikeEditor(table)
    editor.resize(800, 600)
    editor.show()

    sys.exit(app.exec_())
