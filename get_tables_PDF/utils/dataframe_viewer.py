import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
)
from PyQt5.QtCore import Qt


class DataFrameViewer(QMainWindow):
    def __init__(self, dataframes):
        super().__init__()
        self.setWindowTitle("DataFrame Viewer")
        self.dataframes = dataframes  # Liste de DataFrames
        self.current_index = 0

        # Créer le tableau
        self.table = QTableWidget()

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
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        layout.addWidget(button_widget)

        # Définir le widget central
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Afficher le premier DataFrame
        self.display_dataframe()

    def display_dataframe(self):
        """Affiche le DataFrame actuel dans le QTableWidget."""
        if self.dataframes:
            dataframe = self.dataframes[self.current_index]

            self.table.setRowCount(len(dataframe))
            self.table.setColumnCount(len(dataframe.columns))
            self.table.setHorizontalHeaderLabels(dataframe.columns.astype(str))

            for i, row in dataframe.iterrows():
                for j, value in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(value)))

            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()
            self.setWindowTitle(f"DataFrame Viewer - {self.current_index + 1}/{len(self.dataframes)}")

    def show_prev_dataframe(self):
        """Affiche le DataFrame précédent."""
        if self.current_index > 0:
            self.current_index -= 1
            self.display_dataframe()

    def show_next_dataframe(self):
        """Affiche le DataFrame suivant."""
        if self.current_index < len(self.dataframes) - 1:
            self.current_index += 1
            self.display_dataframe()


def show_dataframes(dataframes):
    """Lance le visualiseur de DataFrames."""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    viewer = DataFrameViewer(dataframes)
    viewer.resize(800, 600)
    viewer.show()

    sys.exit(app.exec_())

# import sys
# sys.path.append('get_tables_PDF/utils')
# from dataframe_viewer import show_dataframes

# show_dataframes(df_list)