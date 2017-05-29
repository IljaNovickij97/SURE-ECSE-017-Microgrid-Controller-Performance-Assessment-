from __future__ import unicode_literals
from renewables import *
from voltage import *
from running_cost import *
from data import *
from gui_backend import *


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
        file_open_action = QtWidgets.QAction('Open', self)
        file_open_action.setShortcut('F1')
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
        gr_button.clicked.connect(self.gr)
        h_box.addWidget(gr_button)

        # Renewable Energy Intake button
        rei_button = QtWidgets.QPushButton('Renewable\n Energy\n Intake')
        rei_button.setFixedSize(100, 100)
        rei_button.clicked.connect(self.rei)
        h_box.addWidget(rei_button)

        # Running Cost button
        rc_button = QtWidgets.QPushButton('Running\n Cost')
        rc_button.setFixedSize(100, 100)
        rc_button.clicked.connect(self.rc)
        h_box.addWidget(rc_button)

        # Storage Use button
        su_button = QtWidgets.QPushButton('Storage\n Use')
        su_button.setFixedSize(100, 100)
        su_button.clicked.connect(self.su)
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
        self.tv.setColumnWidth(0, 340)
        self.tv.setColumnWidth(1, 60)
        self.tv.setColumnWidth(2, 60)
        self.tv.setColumnWidth(3, 60)

        self.statusBar()

    def open_file(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        if filename[0] == '':
            return
        self.Data = Data(filename[0])
        self.update_table()
        self.statusBar().showMessage("Data loaded.", 1000)

    def vf(self):
        if self.Data is None:
            self.statusBar().showMessage("No data loaded.", 1000)
            return
        window = NewWindow(parent=self, title='Voltage and Frequency')
        window.setMinimumSize(540, 700)

        # Layout
        v_box = QtWidgets.QVBoxLayout(window.main_widget)

        # Graphs
        hist = Canvas(window.main_widget)
        time_plot = Canvas(window.main_widget)
        VoltageAndFrequency.voltage_hist(self.Data, hist, 0, 20)
        VoltageAndFrequency.voltage_time_plot(self.Data, time_plot, 0)
        v_box.addWidget(hist)
        v_box.addWidget(time_plot)

        # Table
        headers = ['Controller Name', 'Std. Deviation', 'Mean']
        stats = VoltageAndFrequency.voltage_stats(self.Data, 0)
        tm = DataTableModel([[self.Data.controllerName, "%.2f" % stats[0], "%.2f" % stats[1]]], headers,
                            self.main_widget)
        tv = QtWidgets.QTableView()
        tv.setModel(tm)
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)
        vh = tv.verticalHeader()
        vh.setVisible(False)
        v_box.addWidget(tv)
        tv.setColumnWidth(0, 300)
        tv.setColumnWidth(1, 100)
        tv.setColumnWidth(2, 100)

    def gr(self):
        if self.Data is None:
            self.statusBar().showMessage("No data loaded.", 1000)
            return
        self.statusBar().showMessage("This is still a work in progress!", 1000)

    def rei(self):
        if self.Data is None:
            self.statusBar().showMessage("No data loaded.", 1000)
            return

        window = NewWindow(parent=self, title='Renewables')
        window.setMinimumSize(540, 700)

        # Layout
        v_box = QtWidgets.QVBoxLayout(window.main_widget)

        # Graphs
        rpie = Canvas(window.main_widget)
        time_plot = Canvas(window.main_widget)
        Renewables.renewablePie(self.Data, rpie)
        Renewables.renewableTime(self.Data, time_plot)
        v_box.addWidget(rpie)
        v_box.addWidget(time_plot)

    def rc(self):
        if self.Data is None:
            self.statusBar().showMessage("No data loaded.", 1000)
            return
        pass

    def su(self):
        if self.Data is None:
            self.statusBar().showMessage("No data loaded.", 1000)
            return

        # Table
        headers = ['Controller Name', 'Std. Deviation', 'Mean']
        stats = VoltageAndFrequency.voltage_stats(self.Data, 0)
        tm = DataTableModel([[self.Data.controllerName, "%.2f" % stats[0], "%.2f" % stats[1]]], headers,
                            self.main_widget)
        tv = QtWidgets.QTableView()
        tv.setModel(tm)
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)
        vh = tv.verticalHeader()
        vh.setVisible(False)
        v_box.addWidget(tv)
        tv.setColumnWidth(0, 300)
        tv.setColumnWidth(1, 100)
        tv.setColumnWidth(2, 100)
        pass