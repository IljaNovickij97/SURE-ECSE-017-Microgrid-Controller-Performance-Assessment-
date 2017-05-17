import gui
import sys
from PyQt5 import QtCore, QtWidgets

progname = 'Microgrid Controller Assessment Tool'

qApp = QtWidgets.QApplication(sys.argv)
aw = gui.ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()