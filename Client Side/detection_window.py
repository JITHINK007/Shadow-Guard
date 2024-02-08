from PyQt5.QtWidgets import QMainWindow,QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage,QPixmap
from detection import Detection
from threading import Thread

class DetectionWindow(QMainWindow):
    def __init__(self):
        super(DetectionWindow,self).__init__()
        loadUi('UI/detection_window.ui',self)

        self.stop_detection_button.clicked.connect(self.close)
    def create_detection_instance(self,x,y):
        self.detection=Detection(x,y)
    
    @pyqtSlot(QImage)
    def setImage(self,image):
        self.label_detection.setPixmap(QPixmap.fromImage(image))
    
    def start_detection(self):
        self.detection.changePixmap.connect(self.setImage)
        # t1=Thread(target=self.detection.detect_weapon)
        self.detection.start()
        # t1.start()
        self.show()
    def claseEvent(self,event):
        self.detection.running=False
        event.accept()
