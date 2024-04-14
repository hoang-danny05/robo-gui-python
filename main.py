#!C:\Users\Bajan\Documents\Internship\beth-quaing\venv\Scripts\python.exe
import sys
from PySide6 import QtCore, QtWidgets, QtGui
from controller import Controller
import os
import json
import glob

class MainModel(QtCore.QObject):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def about_dialog(self, parent):
        QtWidgets.QMessageBox.about(
            parent,
            f"About the App",
            "This app is in super super beta. Made by Danny Hoang for Hyrel Technologies. Please tell him if anything is super wrong, thank you."
        )

    #interaction events

    def mode_selected(self, item: QtWidgets.QListWidgetItem):
        print(f"mode selected: {item.text()}")
        if (self.modes[item.text()]):
            print("Available")
            QtWidgets.QMessageBox.about(
                self.parent,
                f"{item.text()} Status",
                "This value is set. There should be something here but danny was lazy."
            )
        else:
            print("Not available. Do you want to create your own?")
            response = QtWidgets.QMessageBox.question(
                self.parent,
                f"{item.text()} Status",
                "This part is not currently configured for this type of feeder. Do you want to create a new path?",
                QtWidgets.QMessageBox.StandardButton.Yes,
                QtWidgets.QMessageBox.StandardButton.No
            )
            res = "Yes" if (response == QtWidgets.QMessageBox.StandardButton.Yes) else "No"
            print(f"recieved response: {res}")
        pass

    # if the user adds a new setting for a part
    def add_part_triggered(self): 
        part_name, ok = QtWidgets.QInputDialog().getText(
            self.parent, 
            "QInputDialog.getText()", 
            "Part Name: ", 
            QtWidgets.QLineEdit.EchoMode.Normal,
            QtCore.QDir.home().dirName()
        )

        if ok and part_name: 
            if (os.path.exists(f"./components/{part_name}")):
                QtWidgets.QMessageBox.about(
                    self.parent,
                    "File already exists",
                    "This instruction set already exists. Click on it to edit it."
                )
                pass
            os.mkdir(f"./components/{part_name}")
            ficon : QtGui.QIcon     = QtGui.QIcon(pixmap=QtWidgets.QStyle.SP_MessageBoxCritical)
            self.parent.view.load_modes(QtWidgets.QListWidgetItem(ficon, part_name))
            

            #check if part already exists
            #if exists, prompt that part already exists. 
            #if not exists, create.
        else: 
            pass

    def add_instruction_triggered(self):
        print("asdfasdf")

    # def nav_back(self):
        # self.parent.view.disconnect(self.load)
    
class MainView(QtWidgets.QWidget):
    parent: QtWidgets.QMainWindow
    # component_clicked = QtCore.Signal(QtWidgets.QListWidgetItem)

    # the default starting screen
    """
    SCREENS TO BE LOADED BY THE APPLICATION
    """
    def load_components(self):
        self.list_widget.clear()
        self.add_action.triggered.connect(self.model.add_part_triggered)
        self.parts = []
        ficon : QtGui.QIcon     = QtGui.QIcon(self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_FileIcon))
        self.fpath : str        = "./components/*"
        components : list[str]  = glob.glob(self.fpath)

        for c in components:
            c = c[(len(self.fpath) - 1) :]
            self.parts.append(QtWidgets.QListWidgetItem(ficon, c))

        self.list_widget.itemClicked.connect(self.load_modes)

        for p in self.parts:
            self.list_widget.addItem(p)

    @QtCore.Slot()
    def load_modes(self, component : QtWidgets.QListWidgetItem):
        self.list_widget.itemClicked.disconnect(self.load_modes) #This is no longer the action executed 
        self.add_action.triggered.disconnect(self.model.add_part_triggered)
        self.add_action.triggered.connect(self.model.add_instruction_triggered)
        #add option to add new thing
        comp_name = component.text()
        self.list_widget.itemClicked.connect(lambda feeder : self.load_controller(comp_name, feeder.text()))
        print(f"Hello: {comp_name}")
        self.modes = os.listdir(self.fpath[:-1] + comp_name)
        print(f"Listing directory: {self.fpath[:-1] + comp_name}")
        print(self.modes)
        self.list_widget.clear()
        self.list_widget.addItems(mode.partition(".")[0] for mode in self.modes)
    
    def load_controller(self, component, feeder_type):
        self.add_action.triggered.disconnect(self.model.add_instruction_triggered)
        #i pre did the text() methods, we might not want that.
        print(f"Now configuring {component} with a {feeder_type} feeder.")
        self.stack.setCurrentIndex(1)

    """
    the view init
    """
    def __init__(self, parent: QtWidgets.QMainWindow, model: MainModel):
        super().__init__()
        self.parent = parent
        self.model = model
        self.setLayout(QtWidgets.QVBoxLayout())

        #stacks store a lot of widgets
        self.stack = QtWidgets.QStackedWidget()

        self.list_widget = QtWidgets.QListWidget()
        self.controller = Controller()

        self.stack.addWidget(self.list_widget)
        self.stack.addWidget(self.controller)

        self.layout().addWidget(self.stack)

        #menu bar stuff
        self.add_action = parent.menuBar().addAction("Add")

        self.load_components()
        pass

    """
    Parent Widget Menu Logic
    """
    def renderParent(self):
        menu_bar = self.parent.menuBar()
        #TODO: change this to a menu and add useful stuff here
        file_action = menu_bar.addAction("File")
        file_action.triggered.connect(lambda :print("There are no file options right now."))
        # file_action = menu_bar.addAction("File")
        # file_action.triggered.connect(lambda :print("There are no file options right now."))
        about_action = menu_bar.addAction("About")
        about_action.triggered.connect(lambda : self.parent.model.about_dialog(self.parent))


        ### Tool Bar Stuff
        toolbar = self.parent.addToolBar("Navigation")
        go_back_icon = QtGui.QIcon("./assets/left_undo.xpm")
        go_back_action : QtWidgets.QWidgetAction = toolbar.addAction("Go Back")
        go_back_action.setIcon(go_back_icon)
        go_back_action.setText("Back")

class MainWidget(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        ##### MAINWINDOW COMPONENTS
        self.setWindowTitle("Robot GUI Application")
        # use default status bar
        # you can add perm widgets to the status bar
        self.statusBar().showMessage("Welcome to the Robot GUI")

        self.model = MainModel(self)
        self.view = MainView(self, self.model)
        self.view.renderParent()
        ### Menu Bar Stuff
        self.setCentralWidget(self.view)

app = QtWidgets.QApplication([])

widget = MainWidget()
widget.resize(800, 600)
widget.show()

sys.exit(app.exec())