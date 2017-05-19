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
        self.setMinimumSize(100, 20)
        self.main_widget = QtWidgets.QWidget(self)


        v = QtWidgets.QVBoxLayout(self.main_widget)
        self.graphs = QtWidgets.QVBoxLayout(self.main_widget)
        v.addLayout(self.graphs)
        quitLayout = QtWidgets.QHBoxLayout(self.main_widget)
        quit = QtWidgets.QPushButton(self.main_widget)
        quit.setFixedSize(100, 25)
        quit.setText('Quit')
        quit.setToolTip('Press this to quit')
        quit.clicked.connect(self.closeEvent)
        quitLayout.addWidget(quit)


        v.addLayout(quitLayout)
        v.addStretch(1)

        self.setLayout(v)

        fileOpenAction = QtWidgets.QAction('Open File', self)
        fileOpenAction.triggered.connect(self.openFile)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(fileOpenAction)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def openFile(self):
        name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        self.statusBar().showMessage("Loading!", 3000)
        Data = data.Data(name[0])
        self.setMinimumSize(500, 700)
        self.statusBar().showMessage("Finished Loading! Graphing...", 1000)


        self.sc = Canvas(self.main_widget, width=5, height=4, dpi=100)
        self.cc = Canvas(self.main_widget, width=5, height=4, dpi=100)
        self.graphs.addWidget(self.sc)
        self.graphs.addWidget(self.cc)

        voltage.VoltageAndFrequency.voltage_hist(Data, self.sc, 0, 20)
        voltage.VoltageAndFrequency.voltage_time_plot(Data, self.cc, 0)


class Canvas(FigureCanvas):         # Class used to contain graphs as widget in the PyQt framework
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)



