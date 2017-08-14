from gui import *
import sys
from PyQt5 import QtWidgets

# Setup the main window and application settings

app = QtWidgets.QApplication(sys.argv)
app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
main_window = MainWindow()
main_window.setWindowTitle('Microgrid Controller Assessment Tool')
main_window.show()
sys.exit(app.exec_())

