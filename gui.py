from __future__ import unicode_literals
import matplotlib
from PyQt5 import QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import voltage
import data


class MainWindow(QtWidgets.QMainWindow):    # Main window of the gui.
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.Data = None
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setMinimumSize(540, 250)
        self.setGeometry(0, 30, 540, 220)
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

        # Layout
        v_box = QtWidgets.QVBoxLayout(self.main_widget)
        h_box = QtWidgets.QHBoxLayout(self.main_widget)
        v_box.addLayout(h_box)
        v_box.addStretch()

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

        # Data Table
        self.headers = ['Controller Name', '# Buses', '# DERs', '# Loads']
        tm = DataTableModel([['', '', '', '']], self.headers, self.main_widget)
        self.tv = QtWidgets.QTableView()
        self.tv.setModel(tm)
        v_box.addWidget(self.tv)
        hh = self.tv.horizontalHeader()
        hh.setStretchLastSection(True)
        vh = self.tv.verticalHeader()
        vh.setVisible(False)
        v_box.addStretch()

        self.statusBar()
        self.tv.setColumnWidth(0, 340)
        self.tv.setColumnWidth(1, 60)
        self.tv.setColumnWidth(2, 60)
        self.tv.setColumnWidth(3, 60)

    def open_file(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        self.Data = data.Data(filename[0])
        self.update_table()
        self.statusBar().showMessage("Data loaded.", 1000)

    def vf(self):
        if self.Data is None:
            self.statusBar().showMessage("No data loaded.", 1000)
            return
        window = NewWindow(parent=self, title='Voltage and Frequency')

        # Layout
        v_box = QtWidgets.QVBoxLayout(window.main_widget)

        # Graphs
        hist = Canvas(self.main_widget)
        time_plot = Canvas(self.main_widget)
        voltage.VoltageAndFrequency.voltage_hist(self.Data, hist, 0, 20)
        voltage.VoltageAndFrequency.voltage_time_plot(self.Data, time_plot, 0)
        v_box.addWidget(hist)
        v_box.addWidget(time_plot)

        # Table
        headers = ['Controller Name', 'Std. Deviation', 'Mean']
        stats = voltage.VoltageAndFrequency.voltage_stats(self.Data,0)
        tm = DataTableModel([[self.Data.controllerName, "%.2f" % stats[0], "%.2f" % stats[1]]], headers,
                            self.main_widget)
        tv = QtWidgets.QTableView()
        tv.setModel(tm)
        v_box.addWidget(tv)
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)
        vh = tv.verticalHeader()
        vh.setVisible(False)

        tv.setColumnWidth(0, 300)
        tv.setColumnWidth(1, 100)
        tv.setColumnWidth(2, 100)


    def update_table(self):
        table_data = [[self.Data.controllerName, self.Data.nBus, self.Data.nDer, self.Data.nLoad]]
        print(self.Data.controllerName)
        tm = DataTableModel(table_data, self.headers, self.main_widget)
        self.tv.setModel(tm)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()


class Canvas(FigureCanvas):         # Class used to contain graphs as widget in the PyQt framework
    def __init__(self, parent=None, width=4, height=4, dpi=100):
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
        self.setMinimumSize(540, 800)
        self.move(0, 210)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.main_widget = QtWidgets.QWidget(self)
        self.setWindowTitle(title)
        self.show()
        self.setCentralWidget(self.main_widget)


class DataTableModel(QtCore.QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None):
        super().__init__(parent)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.headerdata[col])
        return QtCore.QVariant()



