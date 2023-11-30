import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from ..Controller.controller import Controller
from main_window import MainWindow
from buttons import *




class ButtonsPannel(qtw.QWidget):

    def __init__(self, controller : Controller, mainWindow : MainWindow):

        super().__init__()
        self.controller = controller
        self.mw = mainWindow
        self.initGUI()

    def initGUI(self):

        layout = qtw.QVBoxLayout()

        load_image_button = LoadImageButton(self.controller, self.mw)
        save_image_button = SaveImageButton(self.controller, self.mw)

        self.setLayout(self.layout)

    

