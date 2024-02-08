from PyQt5.QtWidgets import QMainWindow,QMessageBox
from PyQt5.uic import loadUi
from detection_window import DetectionWindow
from twilio.rest import Client

class SettingsWindow(QMainWindow):
    def __init__(self):
        super(SettingsWindow,self).__init__()
        loadUi('UI/settings_window.ui',self)

        self.detection_window = DetectionWindow()

        
        self.pushButton.clicked.connect(self.go_to_detection)
        self.show()#

    def displayInfo(self):
        self.show()

    def go_to_detection(self):
        if self.detection_window.isVisible():
            print('Detection Window is already open')
        else:
            x=self.sendTo_input.text()
            y=self.location_input.text()
            if y and x:
                sid='AC49af97cd8e4a643400ff119e69fd6080'
                auth='3a903437c91ac2cd627bed926b6eab85'
                client=Client(sid,auth)
                msg='This is a verification message'
                try:
                    client.messages.create(
                        body=msg,
                        from_='+12525074002',
                        to='+91'+x,
                    )
                    self.detection_window.create_detection_instance(x,y)
                    self.detection_window.start_detection()
                except Exception as e:
                    print(f'Error: {e}')
                    print('Create a twilio account and try again')
            else:
                print('Enter all the Fields to start Detecting')
    def closeEvent(self,event):
        if self.detection_window.isVisible():
            self.detection_window.detection.running=False
            self.detection_window.close()
            event.accept()