#!C:\Users\Bajan\Documents\Internship\beth-quaing\venv\Scripts\python.exe
import sys
from PySide6 import QtCore, QtWidgets, QtGui
import os
import json
import glob

class MainWidget(QtWidgets.QMainWindow):
    ###### Screens #####
    def load_home(self):
        self.list_widget.clear()
        self.parts = []
        ficon : QtGui.QIcon     = QtGui.QIcon("file.xpm")
        self.fpath : str        = "./components/*"
        components : list[str]  = glob.glob(self.fpath)

        for c in components:
            c = c[(len(self.fpath) - 1) :]
            self.parts.append(QtWidgets.QListWidgetItem(ficon, c))

        self.list_widget.itemClicked.connect(self.home_item_clicked)

        for p in self.parts:
            self.list_widget.addItem(p)
    
    def load_modes(self, item: QtWidgets.QListWidgetItem):
        print(f"Hello: {item.text()}")
        keys = []
        # print(f"trying to open {self.fpath[:-1] + item.text()} with path {os.getcwd()}")
        with open(self.fpath[:-1] + item.text(), "r") as file:
            attrs : dict = json.load(file)
            keys = attrs.keys()
            print(attrs)
        # self.list_widget.addItems(["test"])
        # it dynamically chaanges the display
        self.list_widget.clear()
        self.list_widget.addItems(keys)

    ##### Actions #####
    def navigate_to(self, load_func):
        self.list_widget.itemClicked.disconnect(self.current_nav)
        self.list_widget.itemClicked.connect(load_func)
        self.navigation_stack.append(self.current_nav)
        self.current_nav = load_func

    def navigate_back(self):
        # print("Going back!")
        if (len(self.navigation_stack) >= 1): 
            self.list_widget.itemClicked.disconnect(self.current_nav)
            previous_page = self.navigation_stack.pop()
            self.current_nav = previous_page
            previous_page()
        else:
            print("refusing to undo")

    def modes_selected(self, item: QtWidgets.QListWidgetItem):
        print(f"mode selected: {item.text()}")
        pass

    #prefix screen-unique methods with the screen name
    def home_item_clicked(self, item: QtWidgets.QListWidgetItem):
        self.load_modes(item)
        self.navigate_to(self.modes_selected)
        # self.list_widget.itemClicked.disconnect(self.previous_page)
        # self.list_widget.itemClicked.connect(self.modes_selected)
        # self.previous_page = self.home_item_clicked

    def __init__(self):
        super().__init__()

        ##### MAINWINDOW COMPONENTS
        # use default status bar
        # you can add perm widgets to the status bar
        self.statusBar().showMessage("Welcome to the Robot GUI")

        menu_bar = self.menuBar()
        #TODO: change this to a menu and add useful stuff here
        file_action = menu_bar.addAction("File")
        file_action.triggered.connect(lambda :print("hello world"))

        toolbar = self.addToolBar("Navigation")
        go_back_icon = QtGui.QIcon("./assets/left-undo.png")
        go_back_action : QtWidgets.QWidgetAction = toolbar.addAction("Go Back")
        go_back_action.setIcon(go_back_icon)
        go_back_action.triggered.connect(self.navigate_back)

        # self.next_page = self.load_modes

        ##### SUBWIDGETS
        self.navigation_stack = []
        self.current_nav = self.load_home

        self.list_widget: QtWidgets.QListWidget = QtWidgets.QListWidget()
        self.load_home()
        self.setCentralWidget(self.list_widget)

app = QtWidgets.QApplication([])

widget = MainWidget()
widget.resize(800, 600)
widget.show()

sys.exit(app.exec())