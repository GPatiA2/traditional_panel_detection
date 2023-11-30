import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from ..Controller.controller import Controller
from main_window import MainWindow
from dialogs import AddFilterDialog

class LoadImageButton(qtw.QPushButton):

    def __init__(self, controller : Controller, mainWindow : MainWindow):

        super().__init__("Load image")
        self.controller = controller
        self.clicked.connect(self.load_image)
        self.mw = mainWindow

    def load_image(self):

        file_name = qtw.QFileDialog.getOpenFileName(self.mw, "Open image", "/home/cvar", "Image files (*.jpg *.png *.jpeg *.bmp *.tif)")
        self.controller.load_image(file_name)

class SaveImageButton(qtw.QPushButton):

    def __init__(self, controller : Controller, mainWindow : MainWindow):

        super().__init__("Save image")
        self.controller = controller
        self.clicked.connect(self.save_image)
        self.mw = mainWindow

    def save_image(self):

        file_name = qtw.QFileDialog.getOpenFileName(self.mw, "Save image", "/home/cvar")
        self.controller.save_image(file_name)

class AddFilterButton(qtw.QPushButton):

    def __init__(self, controller : Controller, mainWindow : MainWindow):

        super().__init__("Add filter")
        self.controller = controller
        self.clicked.connect(self.add_filter)
        self.mw = mainWindow

    def add_filter(self):

        dialog = AddFilterDialog(self.controller, self.mw)
        if dialog.exec():
            filter_added = dialog.get_filter_added()
            self.controller.add_filter(filter_added)
        else:
            filter_added = None
