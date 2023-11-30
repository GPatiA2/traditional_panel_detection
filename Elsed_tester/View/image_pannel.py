import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from ..Controller.controller import Controller
from ..Model.observers import ImageObserver
import numpy as np

class ImagePannel(qtw.QWidget, ImageObserver):

    def __init__(self, controller : Controller):

        super().__init__()
        self.controller = controller
        self.initGUI()
        self.controller.add_image_observer(self)


    def initGUI(self):

        self.layout = qtw.QVBoxLayout()

        self.image  = np.ones((1280,720,3), np.uint8)
        
        label = self.cv2img_to_qt(self.image)

        self.layout.addWidget(label)

        self.setLayout(self.layout)


    def cv2img_to_qt(self, img : np.array):
            
        label = qtw.QLabel()
        label.setSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Ignored)
        label.resize(1280,720)
        label.setAlignment(qtc.Qt.AlignCenter)

        img = np.transpose(img, (1,0,2))

        qImg = qtg.QImage(img.data, img.shape[1], img.shape[0], qtg.QImage.Format_RGB888)
        pixmap = qtg.QPixmap(qImg)
        pixmap = pixmap.scaled(1280, 720, qtc.Qt.KeepAspectRatio)

        label.setPixmap(pixmap)

        return label
    
    def update(self, image : np.array) -> None:
        
        self.image = image
        label = self.cv2img_to_qt(self.image)
        self.clear_layout()
        self.layout.addWidget(label)

    def clear_layout(self):

        num_widgets = self.layout.count()
        while num_widgets > 0:
            self.layout.itemAt(0).widget().setParent(None)
            num_widgets -= 1
