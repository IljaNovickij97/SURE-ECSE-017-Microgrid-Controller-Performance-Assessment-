from __future__ import unicode_literals
import matplotlib
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import voltage
import data


class MainWindow(QtWidgets.QMainWindow):    # Main window of the gui.
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.main_widget = QtWidgets.QWidget(self)

        Data = data.Data('sample.txt')
        l = QtWidgets.QVBoxLayout(self.main_widget)
        sc = Canvas(self.main_widget, width=5, height=4, dpi=100)
        voltage.VoltageAndFrequency.voltage_hist(Data, sc, 0, 20)
        l.addWidget(sc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()


class Canvas(FigureCanvas):         # Class used to contain graphs as widget in the PyQt framework
    def __init__(self, parent=None, width=5, height=4, dpi=100, toolbar=False):
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.axes = self.fig.add_subplot(111)



