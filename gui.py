from __future__ import unicode_literals
from renewables import *
from voltage import *
from data import *
from gui_backend import *
from generation_rejection import *


class MainWindow(QtWidgets.QMainWindow):    # Main window of the gui.
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.data_list = []
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

    def vf(self):
        if self.data_list[0] is None:
            self.statusBar().showMessage("No data loaded.", 1000)
            return

        selected = self.get_selected()
        selected_data = []
        if selected == []:
            selected_data = [self.data_list[0]]
        else:
            for i in range(len(self.data_list)):
                if i in selected:
                    selected_data.append(self.data_list[i])

        window = NewWindow(parent=self, title='Voltage and Frequency')
        window.setMinimumSize(540, 700)

        # Layout
        v_box = QtWidgets.QVBoxLayout(window.main_widget)

        # Graphs
        hist = Canvas(window.main_widget)
        time_plot = Canvas(window.main_widget)
        VoltageAndFrequency.voltage_hist(self.data_list[0], hist, 0, 20)
        VoltageAndFrequency.voltage_time_plot(selected_data, time_plot, 0)
        v_box.addWidget(hist)
        v_box.addWidget(time_plot)

        # Table
        headers = ['Controller Name', 'Std. Deviation', 'Mean']
        stats = VoltageAndFrequency.voltage_stats(self.data_list[0], 0)
        tm = DataTableModel([[self.data_list[0].controllerName, "%.2f" % stats[0], "%.2f" % stats[1]]], headers,
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
        if self.data_list[0] is None:
            self.statusBar().showMessage("No data loaded.", 1000)
            return

        window = NewWindow(parent=self, title='Generation Rejection')
        window.setMinimumSize(540, 400)

        # Layout
        v_box = QtWidgets.QVBoxLayout(window.main_widget)

        # Graphs
        time_plot = Canvas(window.main_widget)
        GenerationRejection.dump_time_plot(self.data_list[0], time_plot)
        v_box.addWidget(time_plot)

        # Table
        headers = ['Controller Name', 'Total Dumped (MWh)']
        stats = GenerationRejection.dump_stats(self.data_list[0])
        tm = DataTableModel([[self.data_list[0].controllerName, "%.2f" % stats[0]]], headers,
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

    def rei(self):
        if self.data_list[0] is None:
            self.statusBar().showMessage("No data loaded.", 1000)
            return

        window = NewWindow(parent=self, title='Renewables')
        window.setMinimumSize(540, 700)

        # Layout
        v_box = QtWidgets.QVBoxLayout(window.main_widget)

        # Graphs
        rpie = Canvas(window.main_widget)
        time_plot = Canvas(window.main_widget)
        Renewables.renewablePie(self.data_list[0], rpie)
        Renewables.renewableTime(self.data_list[0], time_plot)
        v_box.addWidget(rpie)
        v_box.addWidget(time_plot)

    def rc(self):
        if self.data_list[0] is None:
            self.statusBar().showMessage("No data loaded.", 1000)
            return
        self.statusBar().showMessage("This is still a work in progress!", 1000)

    def su(self):
        if self.data_list[0] is None:
            self.statusBar().showMessage("No data loaded.", 1000)
            return

        print(self.get_selected())
        self.statusBar().showMessage("This is still a work in progress!", 1000)

    def open_file(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        if filename[0] == '':
            return
        self.data_list.append(Data(filename[0]))
        self.update_table()
        self.statusBar().showMessage("Data loaded.", 1000)

    def update_table(self):
        table_data = []

        for i in range(len(self.data_list)):
            current_data = [self.data_list[i].controllerName, self.data_list[i].nBus, self.data_list[i].nDer,
                            self.data_list[i].nLoad]
            table_data.append(current_data)

        tm = DataTableModel(table_data, self.headers, self.main_widget)
        self.tv.setModel(tm)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def get_selected(self):
        selected_box = self.tv.selectedIndexes()
        columns = []
        rows = []
        selected = []

        for i in range(len(selected_box)):
            current_row = selected_box[i].row()
            current_column = selected_box[i].column()
            rows.append(current_row)
            columns.append(current_column)

        for i in range(len(selected_box)):
            if columns[i] == 0:
                selected.append(rows[i])

        return selected
