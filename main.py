import sys
from PySide6 import QtCore, QtWidgets, QtGui
# import os
import json
import glob

class MainWidget(QtWidgets.QWidget):

    def item_clicked(self, item: QtWidgets.QListWidgetItem):
        print(f"Hello: {item.text()}")
        with open(self.fpath[:-1] + item.text(), "r") as file:
            attrs = json.load(file)
            print(attrs)

    def __init__(self):
        super().__init__()

        self.parts = []
        list_widget: QtWidgets.QListWidget = QtWidgets.QListWidget()
        ficon : QtGui.QIcon     = QtGui.QIcon("file.xpm")
        self.fpath : str        = "./components/*"
        components : list[str]  = glob.glob(self.fpath)

        for c in components:
            c = c[(len(self.fpath) - 1) :]
            self.parts.append(QtWidgets.QListWidgetItem(ficon, c))

        list_widget.itemClicked.connect(self.item_clicked)

        self.layout = QtWidgets.QVBoxLayout(self)
        for p in self.parts:
            list_widget.addItem(p)
        self.layout.addWidget(list_widget)

app = QtWidgets.QApplication([])

widget = MainWidget()
widget.resize(800, 600)
widget.show()

sys.exit(app.exec())