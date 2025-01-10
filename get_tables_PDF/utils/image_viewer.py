import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class ImageAndTableViewer(QMainWindow):
    def __init__(self, items):
        super().__init__()
        self.setWindowTitle("Image and Table Viewer")
        self.items = items  # Liste de dictionnaires {"image": ..., "settings": ..., "dataframe": ...}
        self.current_index = 0

        # QLabel pour afficher l'image
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        # QLabel pour afficher les settings
        self.settings_label = QLabel(self)
        self.settings_label.setAlignment(Qt.AlignCenter)

        # QTableWidget pour afficher le DataFrame
        self.table = QTableWidget()

        # Boutons de navigation
        self.prev_button = QPushButton("<< Previous")
        self.next_button = QPushButton("Next >>")
        self.prev_button.clicked.connect(self.show_prev_item)
        self.next_button.clicked.connect(self.show_next_item)

        # Layout des boutons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)

        # Layout principal
        image_and_table_layout = QHBoxLayout()
        image_and_table_layout.addWidget(self.image_label, stretch=1)
        image_and_table_layout.addWidget(self.table, stretch=1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(image_and_table_layout)
        main_layout.addWidget(self.settings_label)
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        main_layout.addWidget(button_widget)

        # Définir le widget central
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Afficher le premier élément
        self.display_item()

    def display_item(self):
        """Affiche l'image, les settings et le tableau correspondant à l'élément actuel."""
        if self.items:
            item = self.items[self.current_index]
            pil_image = item["image"].annotated  # PIL image avec annotations
            settings = item["settings"]
            dataframe = item["dataframe"]

            # Afficher l'image
            qimage = self.pil_to_qimage(pil_image)
            pixmap = QPixmap.fromImage(qimage)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.image_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
            else:
                self.image_label.setText("Cannot load image.")

            # Afficher les settings
            self.settings_label.setText(f"Settings: {settings}")

            # Charger le DataFrame dans le QTableWidget
            self.load_dataframe_into_table(dataframe)

    def load_dataframe_into_table(self, dataframe):
        """Charge les données du DataFrame dans le QTableWidget."""
        self.table.setRowCount(len(dataframe))
        self.table.setColumnCount(len(dataframe.columns))
        self.table.setHorizontalHeaderLabels(dataframe.columns.astype(str))

        for i, row in dataframe.iterrows():
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def resizeEvent(self, event):
        """Réajuste l'image lorsque la fenêtre est redimensionnée."""
        self.display_item()
        super().resizeEvent(event)

    def show_prev_item(self):
        """Affiche l'élément précédent."""
        if self.current_index > 0:
            self.current_index -= 1
            self.display_item()

    def show_next_item(self):
        """Affiche l'élément suivant."""
        if self.current_index < len(self.items) - 1:
            self.current_index += 1
            self.display_item()

    def pil_to_qimage(self, pil_image):
        """Convertit une image PIL en QImage."""
        pil_image = pil_image.convert("RGBA")
        data = pil_image.tobytes("raw", "RGBA")
        qimage = QImage(data, pil_image.width, pil_image.height, QImage.Format_RGBA8888)
        return qimage


def show_images_with_tables(items):
    """Lance le visualiseur d'images avec leurs settings et DataFrames associés."""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    viewer = ImageAndTableViewer(items)
    viewer.resize(1200, 600)
    viewer.show()

    sys.exit(app.exec_())
