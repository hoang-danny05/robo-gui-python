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
    X_VALUE =  0b0010
    Y_VALUE =  0b0100
    Z_VALUE =  0b0110
    RX_VALUE = 0b1010
    RY_VALUE = 0b1100
    RZ_VALUE = 0b1110
    

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
                print("X down", value)
            case 0b0011: #(ParamType.X_VALUE.value + Direction.UP.value):
                print("X up", value)
            case 0b0100: 
                print("Y down", value)
            case 0b0101: 
                print("Y up", value)
            case 0b0110: 
                print("Z down", value)
            case 0b0111: 
                print("Z up", value)
            case 0b1010:
                print("RX down", value)
            case 0b1011:
                print("RX up", value)
            case 0b1100: 
                print("RY down", value)
            case 0b1101: 
                print("RY up", value)
            case 0b1110: 
                print("RZ down", value)
            case 0b1111: 
                print("RZ up", value)

class ControllerView(QtWidgets.QWidget):

    input_signal = QtCore.Signal(int, float)

    """
    PARSE MAGNITUDE
        PARSES THE MAGNITUDE INPUT FIELD
        RETURNS A GUARANTEED INTEGER
    """
    def parseMagnitude(self) -> float:
        try:
            mag = float(self.magnitude.text())
            return mag
        except Exception as e:
            print(f"Error processing int: {e}")
            QtWidgets.QMessageBox.warning(
               self, 
               "Invalid Magnitude",
               "The magnitude that you entered is invalid. Please enter an integer or decimal number as input."
            )
            return 0.0
    
    def control_row(self, param: ParamType):
        layout = QtWidgets.QHBoxLayout()

        #left
        left_button = QtWidgets.QPushButton()
        l_ico = self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowDown)
        left_button.setIcon(l_ico)
        left_button.clicked.connect(lambda : self.input_signal.emit(param | Direction.DOWN, self.parseMagnitude()))
        left_button.setFixedSize(50, 30)
        # left_button.clicked.connect(lambda : print("going down!"))

        #right
        right_button = QtWidgets.QPushButton()
        r_ico = self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_ArrowUp)
        right_button.setIcon(r_ico)
        # right_button.clicked.connect(lambda :print("hello"))
        right_button.clicked.connect(lambda : self.input_signal.emit(param | Direction.UP, self.parseMagnitude()))
        right_button.setFixedSize(50, 30)

        layout.addWidget(left_button)
        layout.addWidget(right_button)
        return layout

    def __init__(self):
        super().__init__()

        top_layer_form = QtWidgets.QFormLayout(self)
        self.setLayout(top_layer_form)
        self.title_font = QtGui.QFont()
        self.title_font.setBold(True)
        self.title_font.setPointSize(18)
        title = QtWidgets.QLabel("Robot Training Interface")
        title.setFont(self.title_font)
        top_layer_form.addWidget(title)

        # TAB WIDGET
        tab_widget = QtWidgets.QTabWidget(self)
        top_layer_form.addWidget(tab_widget)

        ## WRF WIDGET
        wrf_widget = QtWidgets.QWidget(tab_widget)
        wrf_form = QtWidgets.QFormLayout(tab_widget)
        wrf_widget.setLayout(wrf_form)
        

        ### PARAMETER ROWS
        paramfont: QtGui.QFont = QtGui.QFont()
        paramfont.setPointSize(15)
        paramfont.setBold(True)
        parameters = ["X", "Y", "Z", "RX", "RY", "RZ"]
        for (ind, param) in enumerate(parameters): 
            param_label = QtWidgets.QLabel(param)
            param_label.setFont(paramfont)
            #make sure that the index matches my binary code
            wrf_form.addRow(param_label, self.control_row(ParamType.X_VALUE + 2*ind if (ind < 3) else ParamType.X_VALUE + 2*ind + 2))
        
        ### MAGNITIDE OF ADJUSTMENT
        mag_layout = QtWidgets.QHBoxLayout()
        self.magnitude = QtWidgets.QLineEdit()
        self.magnitude.setText("1")
        mag_layout.addWidget(self.magnitude)
        mag_label = QtWidgets.QLabel("mm")
        mag_layout.addWidget(mag_label)
        wrf_form.addRow("Adjustment:", mag_layout)

        tab_widget.addTab(wrf_widget, "WRF")
        tab_widget.addTab(QtWidgets.QLabel("WORK IN PROGRESS"), "Joint")
        # self.setLayout(layout)


class Controller(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.model = ControllerModel()
        self.view = ControllerView()
        self.view.input_signal.connect(self.model.input_signal_handler)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().addWidget(self.view)

        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Controller()
    widget.resize(800, 600)
    # widget.show()

    sys.exit(app.exec())