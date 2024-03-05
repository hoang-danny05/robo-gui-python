import sys
from PySide6 import QtCore, QtWidgets, QtGui
from enum import IntEnum
from mecademicpy import robot as Mecademic
import mecademicpy.robot_classes

# InputType = Enum("InputType", ["X_DOWN", "X_UP"])
class Direction(IntEnum):
    DOWN    = 0b0000
    UP      = 0b0001

class ParamType(IntEnum):
    X_VALUE = 0b0010
    

class ControllerModel(QtCore.QObject):
    #this class can accept a signal that takes in a single string as the error message
    #The program must exit
    terminal_error = QtCore.Signal(str)
    #general error
    error = QtCore.Signal(str)
    #error on connection
    connection_error = QtCore.Signal(str)

    def attempt_connect(self):
        self.robot : Mecademic.Robot = Mecademic.Robot()
        try:
            self.robot.Connect(
                address="192.168.0.100",
                enable_synchronous_mode=True, 
                disconnect_on_exception=False
            )
        except mecademicpy.robot_classes.CommunicationError as ce:
            self.connection_error.emit(ce)
            #maybe you can just call this class again
    
    def home_robot(self):
        try:
            self.robot.ActivateAndHome()
        except Exception as e:
            self.terminal_error

    def MoveJoints(self, list):
        print(f"List to move: {list}")
    
    def input_signal_handler(self, type : int, value: float):
        # print(f"equality: {type == (ParamType.X_VALUE + Direction.UP)}")
        match (type):
            case 0b0010: #(ParamType.X_VALUE.value + Direction.DOWN.value):
                print("x down", value)
            case 0b0011: #(ParamType.X_VALUE.value + Direction.UP.value):
                print("x up", value)

class ControllerView(QtWidgets.QWidget):

    input_signal = QtCore.Signal(int, float)

    def control_row(self, param: ParamType):
        layout = QtWidgets.QHBoxLayout()

        #left
        left_button = QtWidgets.QPushButton()
        l_ico = self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowDown)
        left_button.setIcon(l_ico)
        left_button.clicked.connect(lambda : self.input_signal.emit(param | Direction.DOWN, 5))
        # left_button.clicked.connect(lambda : print("going down!"))

        #right
        right_button = QtWidgets.QPushButton()
        r_ico = self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowUp)
        right_button.setIcon(r_ico)
        # right_button.clicked.connect(lambda :print("hello"))
        right_button.clicked.connect(lambda : self.input_signal.emit(param | Direction.UP, 5))

        layout.addWidget(left_button)
        layout.addWidget(right_button)
        return layout

    def __init__(self):
        super().__init__()

        # tab_layout = QtWidgets.QTabWidget()
        # self.()

        wrf_form = QtWidgets.QFormLayout()
        self.setLayout(wrf_form)
        wrf_form.addRow(QtWidgets.QLabel("this is the x row"), self.control_row(ParamType.X_VALUE))

        self.setLayout(wrf_form)


class Controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.model = ControllerModel()
        self.view = ControllerView()
        self.view.input_signal.connect(self.model.input_signal_handler)
        self.setCentralWidget(self.view)

        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Controller()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())