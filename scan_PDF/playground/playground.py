import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QPushButton, QLineEdit, QWidget, QHBoxLayout, QLabel, QMessageBox
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

        # Layout des boutons
        button_layout = QHBoxLayout()
        button_layout.addWidget(delete_col_button)
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

    def handle_key_press(self, event):
        """Gère les pressions de touches pour la suppression des colonnes."""
        if event.key() == Qt.Key_Delete:
            self.delete_column()

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
    df = pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie"],
        "Homme": [10, 15, 20],
        "Femme": [12, 18, 24],
        "Age": [25, 30, 35]
    })

    editor = ExcelLikeEditor(df)
    editor.resize(800, 600)
    editor.show()

    sys.exit(app.exec_())
