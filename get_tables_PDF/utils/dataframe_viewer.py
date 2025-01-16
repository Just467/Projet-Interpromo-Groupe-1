import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QHBoxLayout, QPushButton, QWidget, QLabel
)
from PyQt5.QtCore import Qt

class DataFrameViewer(QMainWindow):
    def __init__(self, dataframes1, dataframes2=None, headers=None):
        super().__init__()
        self.setWindowTitle("DataFrame Viewer")
        
        # Validate and copy DataFrames
        self.dataframes1 = [df.copy() for df in dataframes1]  # First list of DataFrames
        for df in self.dataframes1:
            df.columns = df.columns.astype(str)

        self.dataframes2 = [df.copy() for df in dataframes2] if dataframes2 else None  # Second list of DataFrames (optional)
        if self.dataframes2:
            for df in self.dataframes2:
                df.columns = df.columns.astype(str)

        self.headers = headers if headers else [""] * len(self.dataframes1)  # Headers list
        if len(self.headers) != len(self.dataframes1):
            raise ValueError("The length of headers must match the length of dataframes1.")

        self.current_index = 0

        # Create the tables
        self.table1 = QTableWidget()
        self.table2 = QTableWidget() if self.dataframes2 else None

        # Header label
        self.header_label = QLabel(self.headers[self.current_index])
        self.header_label.setAlignment(Qt.AlignCenter)

        # Navigation buttons
        self.prev_button = QPushButton("<< Previous")
        self.next_button = QPushButton("Next >>")

        self.prev_button.clicked.connect(self.show_prev_dataframe)
        self.next_button.clicked.connect(self.show_next_dataframe)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.header_label)  # Add header label to the layout
        table_layout = QHBoxLayout()
        table_layout.addWidget(self.table1)
        if self.table2:
            table_layout.addWidget(self.table2)

        main_layout.addLayout(table_layout)
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        main_layout.addWidget(button_widget)

        # Set the central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Display the first DataFrame
        self.display_dataframes()

    def display_dataframes(self):
        """Displays the current DataFrames in the QTableWidgets."""
        if self.dataframes1:
            dataframe1 = self.dataframes1[self.current_index]
            self.load_dataframe_into_table(self.table1, dataframe1)

        if self.dataframes2:
            dataframe2 = self.dataframes2[self.current_index]
            self.load_dataframe_into_table(self.table2, dataframe2)

        # Update header label text
        self.header_label.setText(self.headers[self.current_index])
        
        self.setWindowTitle(
            f"DataFrame Viewer - {self.current_index + 1}/{len(self.dataframes1)}"
        )

    def load_dataframe_into_table(self, table, dataframe):
        """Loads a DataFrame into a QTableWidget."""
        table.setRowCount(len(dataframe))
        table.setColumnCount(len(dataframe.columns))

        table.setHorizontalHeaderLabels(dataframe.columns)

        for i, row in dataframe.iterrows():
            for j, value in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(str(value)))

        table.resizeColumnsToContents()
        table.resizeRowsToContents()

    def show_prev_dataframe(self):
        """Displays the previous DataFrames."""
        if self.current_index > 0:
            self.current_index -= 1
            self.display_dataframes()

    def show_next_dataframe(self):
        """Displays the next DataFrames."""
        if self.current_index < len(self.dataframes1) - 1:
            self.current_index += 1
            self.display_dataframes()

def show_dataframes(dataframes1, dataframes2=None, headers=None):
    """Launches the DataFrame viewer."""
    if dataframes2 and len(dataframes1) != len(dataframes2):
        raise ValueError("The two lists of DataFrames must have the same size.")

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    viewer = DataFrameViewer(dataframes1, dataframes2, headers)
    viewer.resize(1200, 600 if dataframes2 else 800)
    viewer.show()

    sys.exit(app.exec_())

# Example usage
# df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
# df2 = pd.DataFrame({'A': [7, 8, 9], 'B': [10, 11, 12]})
# headers = ["First DataFrame", "Second DataFrame"]
# show_dataframes([df1, df2], headers=headers)
