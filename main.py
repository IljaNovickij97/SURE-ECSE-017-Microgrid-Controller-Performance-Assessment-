import gui
import sys
from PyQt5 import QtWidgets

progname = 'Microgrid Controller Assessment Tool'

qApp = QtWidgets.QApplication(sys.argv)
aw = gui.MainWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
