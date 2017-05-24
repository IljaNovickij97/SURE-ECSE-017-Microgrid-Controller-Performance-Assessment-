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
        self.setFixedSize(540, 170)
        self.move(0, 0)
        self.main_widget = QtWidgets.QWidget(self)
        self.ui_setup()
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def ui_setup(self):     # Add main screen widgets here
        # Actions
        file_open_action = QtWidgets.QAction('Open File', self)
        file_open_action.triggered.connect(self.open_file)

        # Menu bar
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('&File')
        file_menu.addAction(file_open_action)

        # Horizontal layout for buttons
        h_box = QtWidgets.QHBoxLayout(self.main_widget)
        h_box.addStretch(1)

        # Voltage and Frequency button
        vf_button = QtWidgets.QPushButton('Voltage\n and\n Frequency')
        vf_button.setFixedSize(100, 100)
        vf_button.clicked.connect(self.vf)
        h_box.addWidget(vf_button)

        # Generation Rejection button
        gr_button = QtWidgets.QPushButton('Generation\n Rejection')
        gr_button.setFixedSize(100, 100)
        h_box.addWidget(gr_button)

        # Renewable Energy Intake button
        rei_button = QtWidgets.QPushButton('Renewable\n Energy\n Intake')
        rei_button.setFixedSize(100, 100)
        h_box.addWidget(rei_button)

        # Running Cost button
        rc_button = QtWidgets.QPushButton('Running\n Cost')
        rc_button.setFixedSize(100, 100)
        h_box.addWidget(rc_button)

        # Storage Use button
        su_button = QtWidgets.QPushButton('Storage\n Use')
        su_button.setFixedSize(100, 100)
        h_box.addWidget(su_button)

    def open_file(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        self.statusBar().showMessage("Loading!", 3000)
        self.Data = data.Data(filename[0])
        self.statusBar().showMessage("Data Loaded!")

    def vf(self):
        window = NewWindow(parent=self, title='Voltage and Frequency')

        # Layout
        h_box = QtWidgets.QHBoxLayout(window.main_widget)
        text_box = QtWidgets.QVBoxLayout(window.main_widget)
        graphs = QtWidgets.QVBoxLayout(window.main_widget)
        h_box.addLayout(graphs)
        h_box.addLayout(text_box)

        # Graphs
        hist = Canvas(self.main_widget)
        time_plot = Canvas(self.main_widget)
        voltage.VoltageAndFrequency.voltage_hist(self.Data, hist, 0, 20)
        voltage.VoltageAndFrequency.voltage_time_plot(self.Data, time_plot, 0)
        graphs.addWidget(hist)
        graphs.addWidget(time_plot)

        #Text
        bold_font = QtGui.QFont()
        bold_font.setBold(True)
        std = QtWidgets.QLabel(window.main_widget)
        std_val = QtWidgets.QLabel(window.main_widget)
        mean = QtWidgets.QLabel(window.main_widget)
        mean_val = QtWidgets.QLabel(window.main_widget)
        stats = voltage.VoltageAndFrequency.voltage_stats(self.Data, 0)
        std.setText("Standard Deviation:")
        std.setFont(bold_font)
        std_val.setText("%.2f" % stats[0])
        mean.setText("Mean:")
        mean.setFont(bold_font)
        mean_val.setText("%.2f" % stats[1])
        text_box.addWidget(std)
        text_box.addWidget(std_val)
        text_box.addWidget(mean)
        text_box.addWidget(mean_val)
        text_box.addStretch()


    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()


class Canvas(FigureCanvas):         # Class used to contain graphs as widget in the PyQt framework
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class NewWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, title='New Window'):
        super(NewWindow, self).__init__(parent)
        self.setMinimumSize(540, 600)
        self.move(0, 210)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.main_widget = QtWidgets.QWidget(self)
        self.setWindowTitle(title)
        self.show()
        self.setCentralWidget(self.main_widget)


