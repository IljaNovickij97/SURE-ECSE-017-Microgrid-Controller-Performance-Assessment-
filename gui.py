from __future__ import unicode_literals
import matplotlib
from PyQt5 import QtCore, QtWidgets, QtGui
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
        self.setMinimumSize(400, 600)
        self.main_widget = QtWidgets.QWidget(self)

        # name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        # print(name[0])
        # Data = data.Data(name[0])
        Data = data.Data('sample.txt')
        l = QtWidgets.QVBoxLayout(self.main_widget)
        l.setAlignment(QtCore.Qt.AlignTop)
        sc = Canvas(self.main_widget, width=5, height=4, dpi=100)
        voltage.VoltageAndFrequency.voltage_hist(Data, sc, 0, 20)
        l.addWidget(sc)
        cc = Canvas(self.main_widget, width=5, height=4, dpi=100)
        voltage.VoltageAndFrequency.voltage_time_plot(Data, cc, 0)
        l.addWidget(cc)
        quit = QtWidgets.QPushButton(self.main_widget)
        quit.setFixedSize(100, 25)
        quit.setText('Quit')
        quit.clicked.connect(self.closeEvent)
        l.addWidget(quit)

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



