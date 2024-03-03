import sys
from PySide6 import QtCore, QtWidgets, QtGui
# import os
import glob

# class ComponentList(QtWidgets.QListWidget):
#     def __init__(self):
#         super().__init__()


class MyWidget(QtWidgets.QWidget):
    def item_selected(item):
        print("asdfasdfas")
        print(item)

    def __init__(self):
        super().__init__()

        self.parts = []
        list_widget: QtWidgets.QListWidget = QtWidgets.QListWidget()
        ficon : QtGui.QIcon     = QtGui.QIcon("file.xpm")
        fpath : str             = "./components/*"
        components : list[str]  = glob.glob(fpath)

        for c in components:
            c = c[(len(fpath) - 1) :]
            self.parts.append(QtWidgets.QListWidgetItem(ficon, c))

        list_widget.itemClicked = self.item_selected

        self.layout = QtWidgets.QVBoxLayout(self)
        for p in self.parts:
            list_widget.addItem(p)
        self.layout.addWidget(list_widget)

app = QtWidgets.QApplication([])

widget = MyWidget()
widget.resize(800, 600)
widget.show()

sys.exit(app.exec())