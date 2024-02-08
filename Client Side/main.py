from PyQt5.QtWidgets import QApplication
import sys
from settings_window import SettingsWindow

app=QApplication(sys.argv)
mainwindow=SettingsWindow()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
