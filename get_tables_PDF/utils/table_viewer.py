import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QSlider, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt


class SimpleTableViewer(QMainWindow):
    def __init__(self, dataframe):
        super().__init__()
        self.setWindowTitle("Simple Table Viewer")
        self.dataframe = dataframe

        # Créer le tableau
        self.table = QTableWidget()
        self.load_dataframe_into_table()

        # Slider pour zoom/dézoom
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(50, 200)  # Zoom entre 50% et 200%
        self.zoom_slider.setValue(100)  # Zoom initial à 100%
        self.zoom_slider.valueChanged.connect(self.adjust_zoom)

        # Étiquette pour afficher le pourcentage de zoom
        self.zoom_label = QLabel("Zoom: 100%")

        # Disposition du slider et de l'étiquette
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("Zoom:"))
        slider_layout.addWidget(self.zoom_slider)
        slider_layout.addWidget(self.zoom_label)

        # Disposition principale
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        slider_widget = QWidget()
        slider_widget.setLayout(slider_layout)
        layout.addWidget(slider_widget)

        # Définir le widget central
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_dataframe_into_table(self):
        """Charge les données du DataFrame dans le QTableWidget."""
        self.table.setRowCount(len(self.dataframe))
        self.table.setColumnCount(len(self.dataframe.columns))
        self.table.setHorizontalHeaderLabels(self.dataframe.columns)

        for i, row in self.dataframe.iterrows():
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.table.setItem(i, j, item)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.setWordWrap(True)  # Permet d'ajuster le texte dans les cellules

    def adjust_zoom(self):
        """Ajuste le zoom du tableau en fonction de la position du slider."""
        zoom_factor = self.zoom_slider.value()
        self.zoom_label.setText(f"Zoom: {zoom_factor}%")
        font = self.table.font()
        font.setPointSize(int(zoom_factor / 10))  # Ajuste la taille de la police
        self.table.setFont(font)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()


def show_table(dataframe):
    """Fonction utilitaire pour afficher un DataFrame avec SimpleTableViewer."""
    # dataframe.columns = dataframe.columns.astype(str)
    app = QApplication.instance()  # Vérifie si une instance de QApplication existe déjà
    if not app:  # Si aucune instance n'existe, on la crée
        app = QApplication(sys.argv)
    
    viewer = SimpleTableViewer(dataframe)
    viewer.resize(800, 600)
    viewer.show()

    # Exécute l'application sans bloquer l'exécution globale
    app.exec_()

# import sys
# sys.path.append('get_tables_PDF/utils')
# from table_viewer import show_table

# data = {
#     "Name": ["Alice", "Bob", "Charlie"],
#     "Age": [25, 30, 35],
#     "Score": [85, 90, 95]
# }
# df = pd.DataFrame(data)

# show_table(df)