import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QHBoxLayout, QPushButton, QWidget, QLabel
)
from PyQt5.QtCore import Qt


class DataFrameViewer(QMainWindow):
    def __init__(self, dataframes1, dataframes2=None):
        super().__init__()
        self.setWindowTitle("DataFrame Viewer")
        self.dataframes1 = dataframes1  # Première liste de DataFrames
        self.dataframes2 = dataframes2  # Seconde liste de DataFrames (optionnelle)
        self.current_index = 0

        # Créer les tableaux
        self.table1 = QTableWidget()
        self.table2 = QTableWidget() if self.dataframes2 else None

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
        main_layout = QVBoxLayout()
        table_layout = QHBoxLayout()
        table_layout.addWidget(self.table1)
        if self.table2:
            table_layout.addWidget(self.table2)

        main_layout.addLayout(table_layout)
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        main_layout.addWidget(button_widget)

        # Définir le widget central
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Afficher le premier DataFrame
        self.display_dataframes()

    def display_dataframes(self):
        """Affiche les DataFrames actuels dans les QTableWidgets."""
        if self.dataframes1:
            dataframe1 = self.dataframes1[self.current_index]
            self.load_dataframe_into_table(self.table1, dataframe1)

        if self.dataframes2:
            dataframe2 = self.dataframes2[self.current_index]
            self.load_dataframe_into_table(self.table2, dataframe2)

        self.setWindowTitle(
            f"DataFrame Viewer - {self.current_index + 1}/{len(self.dataframes1)}"
        )

    def load_dataframe_into_table(self, table, dataframe):
        """Charge un DataFrame dans un QTableWidget."""
        table.setRowCount(len(dataframe))
        table.setColumnCount(len(dataframe.columns))
        print(dataframe.columns)
        try:
            table.setHorizontalHeaderLabels(dataframe.columns.astype(str))
        except:
            None

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
        if self.current_index < len(self.dataframes1) - 1:
            self.current_index += 1
            self.display_dataframes()


def show_dataframes(dataframes1, dataframes2=None):
    """Lance le visualiseur de DataFrames."""
    if dataframes2 and len(dataframes1) != len(dataframes2):
        raise ValueError("Les deux listes de DataFrames doivent avoir la même taille.")

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    viewer = DataFrameViewer(dataframes1, dataframes2)
    viewer.resize(1200, 600 if dataframes2 else 800)
    viewer.show()

    sys.exit(app.exec_())

# import sys
# sys.path.append('get_tables_PDF/utils')
# from dataframe_viewer import show_dataframes

# show_dataframes(df_list)