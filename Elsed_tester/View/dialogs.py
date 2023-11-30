import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from ..Controller.controller import Controller
from main_window import MainWindow

class AddFilterDialog(qtw.QDialog):

    def __init__(self, controller : Controller, mainWindow : MainWindow):

        super().__init__()
        self.controller = controller
        self.mw = mainWindow
        self.initGUI()
        self.filter_added = False

    def initGUI(self):

        self.layout = qtw.QHBoxLayout()

        self.av_filters  = self.controller.get_available_filters()
        for f in self.av_filters.items():
            f_button = qtw.QPushButton(f[0])
            f_button.clicked.connect(lambda : self.prompt_filter_creation_dialog(f[0], f[1]))

    def get_filter_added(self):

        return self.filter_added

    def prompt_filter_creation_dialog(self, filter_name : str, filter_class : type):

        dialog = FilterCreationDialog(filter_name, filter_class, self.controller, self)
        
        if dialog.exec():
            self.filter_added = dialog.get_filter_added()
        else:
            self.filter_added = None

class FilterCreationDialog(qtw.QDialog):

    def __init__(self, filter_name : str, filter_class : type, controller : Controller, add_filter_dialog : AddFilterDialog):

        super().__init__()
        self.filter_name = filter_name
        self.filter_class = filter_class
        self.controller = controller
        self.add_filter_dialog = add_filter_dialog
        self.initGUI()

    def initGUI(self):

        layout = qtw.QVBoxLayout()
        
        fields_widget = qtw.QWidget()
        fields_layout = qtw.QHBoxLayout()
        for param in self.filter_class.params:
            param_label = qtw.QLabel(param)
            param_input = qtw.QLineEdit()
            fields_layout.addWidget(param_label)
            fields_layout.addWidget(param_input)

        fields_widget.setLayout(fields_layout)
        layout.addWidget(fields_widget)

        buttons_widget = qtw.QWidget()
        buttons_layout = qtw.QHBoxLayout()
        ok_button = qtw.QPushButton("Ok")
        ok_button.clicked.connect(self.save_filter)
        cancel_button = qtw.QPushButton("Cancel")
        cancel_button.clicked.connect(self.cancel)
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        buttons_widget.setLayout(buttons_layout)

        layout.addWidget(buttons_widget)
        

            
    
