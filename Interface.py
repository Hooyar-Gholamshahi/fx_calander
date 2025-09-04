import sys
from pymongo import MongoClient
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget
from PyQt6.QtGui import QStandardItemModel, QStandardItem
import os
from dotenv import load_dotenv, find_dotenv
from larg_db import cursor


load_dotenv(find_dotenv())
password = os.environ.get("mongo_pwd")
# ---- اتصال به MongoDB ----
connection_string = f"mongodb+srv://hooyargholamshahibiz:{password}@poseidon.grrgsbp.mongodb.net/?retryWrites=true&w=majority&appName=Poseidon"
client = MongoClient(connection_string)
db = client["fxstreet_db"]
collection = db["large_db"]

# ---- کوئری نمونه (اینجا فیلتر دلخواه بذار) ----

documents = list(cursor)  # لیست دیکشنری

# ---- GUI ----
class DatabaseViewer(QMainWindow):
    def __init__(self, documents):
        super().__init__()
        self.setWindowTitle("Database Viewer - PyQt6")
        self.resize(900, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.table = QTableView()
        layout.addWidget(self.table)

        self.model = QStandardItemModel()
        self.load_data(documents)

        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()

    def load_data(self, documents):
        if not documents:
            return
        headers = list(documents[0].keys())
        self.model.setColumnCount(len(headers))
        self.model.setHorizontalHeaderLabels(headers)

        for doc in documents:
            items = [QStandardItem(str(doc.get(h, ""))) for h in headers]
            self.model.appendRow(items)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = DatabaseViewer(documents)
    viewer.show()
    sys.exit(app.exec())
