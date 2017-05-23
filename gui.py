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
        self.setFixedSize(540, 170)
        self.main_widget = QtWidgets.QWidget(self)

        fileOpenAction = QtWidgets.QAction('Open File', self)
        fileOpenAction.triggered.connect(self.openFile)
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(fileOpenAction)

        hbox = QtWidgets.QHBoxLayout(self.main_widget)
        hbox.addStretch(1)

        self.vf_button = QtWidgets.QPushButton('Voltage\n and\n Frequency')
        self.vf_button.setFixedSize(100, 100)
        self.vf_button.clicked.connect(self.voltagew)
        hbox.addWidget(self.vf_button)

        gr_button = QtWidgets.QPushButton('Generation\n Rejection')
        gr_button.setFixedSize(100, 100)
        hbox.addWidget(gr_button)

        rei_button = QtWidgets.QPushButton('Renewable\n Energy\n Intake')
        rei_button.setFixedSize(100, 100)
        hbox.addWidget(rei_button)

        rc_button = QtWidgets.QPushButton('Running\n Cost')
        rc_button.setFixedSize(100, 100)
        hbox.addWidget(rc_button)

        su_button = QtWidgets.QPushButton('Storage\n Use')
        su_button.setFixedSize(100, 100)
        hbox.addWidget(su_button)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def openFile(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        self.statusBar().showMessage("Loading!", 3000)
        self.Data = data.Data(filename[0])
        self.statusBar().showMessage("Data Loaded!")

    def voltagew(self):
        newWindow(self.Data, parent=self, title='Voltage and Frequency')


class Canvas(FigureCanvas):         # Class used to contain graphs as widget in the PyQt framework
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class newWindow(QtWidgets.QMainWindow):
    def __init__(self, Data, parent=None, title='New Window'):
        super(newWindow, self).__init__(parent)

        self.setMinimumSize(400, 600)
        self.main_widget = QtWidgets.QWidget(self)
        self.setWindowTitle(title)
        self.show()
        sc = Canvas(self.main_widget, width=5, height=4, dpi=100)
        cc = Canvas(self.main_widget, width=5, height=4, dpi=100)

        graphs = QtWidgets.QVBoxLayout(self.main_widget)
        # graphs.setStretch(1)

        voltage.VoltageAndFrequency.voltage_hist(Data, sc, 0, 20)
        voltage.VoltageAndFrequency.voltage_time_plot(Data, cc, 0)

        graphs.addWidget(sc)
        graphs.addWidget(cc)
        
        self.setCentralWidget(self.main_widget)


