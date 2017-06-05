from gui import *
import sys
from PyQt5 import QtWidgets

progname = 'Microgrid Controller Assessment Tool'


qApp = QtWidgets.QApplication(sys.argv)
qApp.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
aw = MainWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())

