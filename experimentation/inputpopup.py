import sys
from PySide6 import QtCore, QtWidgets, QtGui
# from controller import Controller

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.button.clicked.connect(lambda : self.show_popup())
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)
        # self.controller = Controller()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)
    
    def show_popup(self):
        text, ok = QtWidgets.QInputDialog().getText(self, "TITLELLLLE", "Who asked?", QtWidgets.QLineEdit.EchoMode.Normal, QtCore.QDir().home().dirName())
        print(text,  ok)
        pass

    @QtCore.Slot()
    def magic(self):
        print("hi")
        self.text.setText("please")
    

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())