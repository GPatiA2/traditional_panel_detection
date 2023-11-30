
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from bottom_pannel import BottomPannel
from buttons_pannel import ButtonsPannel
from image_pannel import ImagePannel
from ..Controller.controller import Controller

class MainWindow(qtw.QWidget):
    
    def __init__(self, controller : Controller):
        super().__init__()
        self.controller = controller
        self.initGUI()

    def initGUI(self):

        main_layout = qtw.QVBoxLayout()

        central_pannel = qtw.QWidget()

        central_pannel_layout = qtw.QHBoxLayout()

        buttons_pannel = ButtonsPannel(self.controller)
        img_pannel     = ImagePannel(self.controller)

        central_pannel_layout.addWidget(buttons_pannel)
        central_pannel_layout.addWidget(img_pannel)

        central_pannel.setLayout(central_pannel_layout)

        main_layout.addWidget(central_pannel)
        ####

        bottom_pannel = BottomPannel(img_pannel, self.controller)
        main_layout.addWidget(bottom_pannel)

        self.setLayout(main_layout)
        self.setWindowTitle("Filter tester")
    
