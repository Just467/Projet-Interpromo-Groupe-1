import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QHBoxLayout, QPushButton, QWidget, QLabel, QScrollArea
)
from PyQt5.QtCore import Qt


class DataFrameViewer(QMainWindow):
    def __init__(self, dataframes):
        """
        Affiche les raw_df à gauche et les processed_df (verticalement) à droite.

        Args:
            dataframes (dict): Un dictionnaire où chaque clé correspond à :
                - "raw_df": Le DataFrame brut.
                - "processed_df": Une liste de DataFrames traités.
        """
        super().__init__()
        self.setWindowTitle("DataFrame Viewer")
        self.dataframes = dataframes
        self.keys = list(dataframes.keys())
        self.current_index = 0

        # Créer les tableaux
        self.raw_table = QTableWidget()
        self.split_table_container = QScrollArea()
        self.split_table_container.setWidgetResizable(True)
        self.split_table_widget = QWidget()
        self.split_table_layout = QVBoxLayout()
        self.split_table_widget.setLayout(self.split_table_layout)
        self.split_table_container.setWidget(self.split_table_widget)

        # Boutons de navigation
        self.prev_button = QPushButton("<< Previous")
        self.next_button = QPushButton("Next >>")
        self.prev_button.clicked.connect(self.show_prev_dataframe)
        self.next_button.clicked.connect(self.show_next_dataframe)

        # Layout des boutons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)

        # Layout principal
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.raw_table)
        main_layout.addWidget(self.split_table_container)

        final_layout = QVBoxLayout()
        final_layout.addLayout(main_layout)
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        final_layout.addWidget(button_widget)

        # Définir le widget central
        container = QWidget()
        container.setLayout(final_layout)
        self.setCentralWidget(container)

        # Afficher le premier DataFrame
        self.display_dataframes()

    def clear_split_table_layout(self):
        """Réinitialise le layout des processed_df pour éviter les conflits."""
        while self.split_table_layout.count():
            child = self.split_table_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def display_dataframes(self):
        """Affiche les DataFrames actuels dans les QTableWidgets."""
        key = self.keys[self.current_index]
        data = self.dataframes[key]

        # Afficher la raw_df à gauche
        self.load_dataframe_into_table(self.raw_table, data["raw_df"])

        # Réinitialiser le layout des processed_df
        self.clear_split_table_layout()

        # Afficher les processed_df verticalement à droite
        for df in data["processed_df"]:
            table = QTableWidget()
            self.load_dataframe_into_table(table, df)
            self.split_table_layout.addWidget(table)

        self.setWindowTitle(
            f"DataFrame Viewer - {self.current_index + 1}/{len(self.keys)}"
        )

    def load_dataframe_into_table(self, table, dataframe):
        """Charge un DataFrame dans un QTableWidget."""
        if dataframe.empty:
            table.setRowCount(0)
            table.setColumnCount(0)
            table.setHorizontalHeaderLabels([])
            return

        table.setRowCount(len(dataframe))
        table.setColumnCount(len(dataframe.columns))
        table.setHorizontalHeaderLabels(dataframe.columns.astype(str))

        for i, row in dataframe.iterrows():
            for j, value in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(str(value)))

        table.resizeColumnsToContents()
        table.resizeRowsToContents()

    def show_prev_dataframe(self):
        """Affiche les DataFrames précédents."""
        if self.current_index > 0:
            self.current_index -= 1
            self.display_dataframes()

    def show_next_dataframe(self):
        """Affiche les DataFrames suivants."""
        if self.current_index < len(self.keys) - 1:
            self.current_index += 1
            self.display_dataframes()


def show_processed_dataframes(processed_data):
    """Lance le visualiseur de DataFrames."""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    viewer = DataFrameViewer(processed_data)
    viewer.resize(1400, 800)
    viewer.show()

    sys.exit(app.exec_())