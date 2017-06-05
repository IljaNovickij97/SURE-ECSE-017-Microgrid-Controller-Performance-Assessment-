from __future__ import unicode_literals
from renewables import *
from voltage_frequency import *
from running_cost import *
from data import *
from gui_backend import *
from generation_rejection import *

from running_cost import *

from storage_use import *



class MainWindow(QtWidgets.QMainWindow):    # Main window of the gui.
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.data_list = []
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setMinimumHeight(250)
        self.setFixedWidth(540)
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
        self.tv.setColumnWidth(0, 340)
        self.tv.setColumnWidth(1, 60)
        self.tv.setColumnWidth(2, 60)
        self.tv.setColumnWidth(3, 60)

        self.statusBar()

    def vf(self):
        if not self.data_list:
            self.statusBar().showMessage("No data loaded.", 1000)
            return

        selected_data = self.get_selected()

        window = NewWindow(parent=self, title='Voltage and Frequency')
        window.setMinimumSize(1080, 700)


        # Layout
        v_box = QtWidgets.QVBoxLayout(window.main_widget)
        h_box = QtWidgets.QHBoxLayout(window.main_widget)
        v_box_left = QtWidgets.QVBoxLayout(window.main_widget)
        v_box_right = QtWidgets.QVBoxLayout(window.main_widget)

        # Histogram width
        width = 0.6/len(selected_data)

        # VOLTAGE
        # Graphs
        hist_left = Canvas(window.main_widget)
        toolbar = NavigationToolbar(hist_left, window, coordinates=False)
        time_plot_left = Canvas(window.main_widget)
        time_plot_left.setup_toolbar(toolbar)
        time_plot_left.mouseDoubleClickEvent = time_plot_left.set_toolbar_active
        hist_left.setup_toolbar(toolbar)
        hist_left.mouseDoubleClickEvent = hist_left.set_toolbar_active

        v_box.addWidget(toolbar)
        v_box.addLayout(h_box)

        VoltageAndFrequency.voltage_hist(selected_data, hist_left, 0, width)
        VoltageAndFrequency.voltage_time_plot(selected_data, time_plot_left, 0)
        v_box_left.addWidget(hist_left)
        v_box_left.addWidget(time_plot_left)

        # Table
        headers = ['Controller Name', 'Std. Deviation', 'Mean']
        table_data_left = []
        for i in range(len(selected_data)):
            stats = VoltageAndFrequency.voltage_stats(selected_data[i], 0)
            current_data = [selected_data[i].controllerName, "%.2f" % stats[0], "%.2f" % stats[1]]
            table_data_left.append(current_data)

        tm_left = DataTableModel(table_data_left, headers, self.main_widget)
        tv_left = QtWidgets.QTableView()
        tv_left.setModel(tm_left)
        hh_left = tv_left.horizontalHeader()
        hh_left.setStretchLastSection(True)
        vh_left = tv_left.verticalHeader()
        vh_left.setVisible(False)
        v_box_left.addWidget(tv_left)
        tv_left.setColumnWidth(0, 300)
        tv_left.setColumnWidth(1, 100)
        tv_left.setColumnWidth(2, 100)

        # FREQUENCY
        # Graphs
        hist_right = Canvas(window.main_widget)
        time_plot_right = Canvas(window.main_widget)
        VoltageAndFrequency.frequency_hist(selected_data, hist_right, 0, width)
        VoltageAndFrequency.frequency_time_plot(selected_data, time_plot_right, 0)
        time_plot_right.setup_toolbar(toolbar)
        time_plot_right.mouseDoubleClickEvent = time_plot_right.set_toolbar_active
        hist_right.setup_toolbar(toolbar)
        hist_right.mouseDoubleClickEvent = hist_right.set_toolbar_active
        v_box_right.addWidget(hist_right)
        v_box_right.addWidget(time_plot_right)

        # Table
        headers = ['Controller Name', 'Std. Deviation', 'Mean']
        table_data_right = []
        for i in range(len(selected_data)):
            stats = VoltageAndFrequency.frequency_stats(selected_data[i], 0)
            current_data = [selected_data[i].controllerName, "%.2f" % stats[0], "%.2f" % stats[1]]
            table_data_right.append(current_data)

        tm_right = DataTableModel(table_data_right, headers, self.main_widget)
        tv_right = QtWidgets.QTableView()
        tv_right.setModel(tm_right)
        hh_right = tv_right.horizontalHeader()
        hh_right.setStretchLastSection(True)
        vh_right = tv_right.verticalHeader()
        vh_right.setVisible(False)
        v_box_right.addWidget(tv_right)
        tv_right.setColumnWidth(0, 300)
        tv_right.setColumnWidth(1, 100)
        tv_right.setColumnWidth(2, 100)

        h_box.addLayout(v_box_left)
        h_box.addLayout(v_box_right)

    def gr(self):
        if not self.data_list:
            self.statusBar().showMessage("No data loaded.", 1000)
            return

        selected_data = self.get_selected()

        window = NewWindow(parent=self, title='Generation Rejection')
        window.setMinimumSize(540, 500)

        # Layout
        v_box = QtWidgets.QVBoxLayout(window.main_widget)

        # Graphs
        time_plot = Canvas(window.main_widget)
        toolbar = NavigationToolbar(time_plot, window, coordinates=False)
        GenerationRejection.dump_time_plot(selected_data, time_plot)
        v_box.addWidget(toolbar)
        v_box.addWidget(time_plot)

        # Table
        table_data = []
        for i in range(len(selected_data)):
            stats = GenerationRejection.dump_stats(selected_data[i])
            current_data = [selected_data[i].controllerName, "%.5f" % stats[0]]
            table_data.append(current_data)

        headers = ['Controller Name', 'Total Dumped (MWh)']
        tm = DataTableModel(table_data, headers, self.main_widget)
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
        if not self.data_list:
            self.statusBar().showMessage("No data loaded.", 1000)
            return

        selected_data = self.get_selected()

        n_pies = len(selected_data)
        window = NewWindow(parent=self, title='Renewables')
        window.setMinimumSize(450*n_pies, 400)

        # Layout
        v_box = QtWidgets.QVBoxLayout(window.main_widget)
        pie_box = QtWidgets.QHBoxLayout(window.main_widget)
        table_box = QtWidgets.QHBoxLayout(window.main_widget)

        # Graphs
        canvas_list = []
        for i in range(n_pies):
            canvas_list.append(Canvas(window.main_widget, width=3.5))
            Renewables.renewablePie(selected_data[i], canvas_list[i])
            pie_box.addWidget(canvas_list[i])

        # Table
        table_data = []
        for i in range(len(selected_data)):
            stats = Renewables.renewable_stats(selected_data[i])
            current_data = [selected_data[i].controllerName, "%.2f" % stats[0], "%.2f" % stats[1], "%.2f" % stats[2],
                            "%.2f" % stats[3], "%.2f" % stats[4], "%.2f" % stats[5], "%.2f" % stats[6]]
            table_data.append(current_data)

        headers = ['Controller Name', 'Wind (MWh)', 'Hydro (MWh)', 'PV (MWh)', 'Diesel (MWh)', 'Gas (MWh)',
                   'Renewable (MWh)', 'Total (MWh)']
        tm = DataTableModel(table_data, headers, self.main_widget)
        tv = QtWidgets.QTableView()
        tv.setModel(tm)
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)
        vh = tv.verticalHeader()
        vh.setVisible(False)
        table_box.addWidget(tv)
        tv.setColumnWidth(0, 100)
        tv.setColumnWidth(1, 50*n_pies)
        tv.setColumnWidth(2, 50*n_pies)
        tv.setColumnWidth(3, 50*n_pies)
        tv.setColumnWidth(4, 50*n_pies)
        tv.setColumnWidth(5, 50*n_pies)
        tv.setColumnWidth(6, 50*n_pies)

        v_box.addLayout(pie_box)
        v_box.addLayout(table_box)

    def rc(self):
        if not self.data_list:
            self.statusBar().showMessage("No data loaded.", 1000)
            return

        selected_data = self.get_selected()

        window = NewWindow(parent=self, title='Running Costs')
        window.setMinimumSize(740, 500)

        # Layout
        v_box = QtWidgets.QVBoxLayout(window.main_widget)
        table_box = QtWidgets.QHBoxLayout(window.main_widget)

        # Graphs
        pwr_out = Canvas(window.main_widget)
        runningCost.basicCalc(selected_data)
        runningCost.pwrGen(selected_data, pwr_out)
        v_box.addWidget(pwr_out)

        # Table
        toolbar = NavigationToolbar(pwr_out, window, coordinates=False)
        v_box.addWidget(toolbar)

        headers = ['Controller Name', 'Fuel Consumption(L)', 'On/Off Switching', 'Average Ramping\n(MW/s)', 'Max Ramping\n(MW/s)',
                   'Peak Power\n(Grid Connected) (MW)']
        runningCost.ramping(selected_data)
        table_data = runningCost.rcStats(selected_data)

        for i in range(len(selected_data)):
            table_data[i].insert(0, selected_data[i].controllerName)

        tm = DataTableModel(table_data, headers, self.main_widget)
        tv = QtWidgets.QTableView()
        tv.setModel(tm)
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)
        vh = tv.verticalHeader()
        vh.setVisible(False)
        v_box.addWidget(tv)
        tv.setColumnWidth(0, 110)
        tv.setColumnWidth(1, 120)
        tv.setColumnWidth(2, 120)
        tv.setColumnWidth(3, 120)
        tv.setColumnWidth(4, 120)
        tv.setColumnWidth(5, 120)

        v_box.addLayout(table_box)

    def su(self):
        if not self.data_list:
            self.statusBar().showMessage("No data loaded.", 1000)
            return

        selected_data = self.get_selected()
        window = NewWindow(parent=self, title='Storage Use')
        window.setMinimumSize(540, 500)

        # Layout
        v_box = QtWidgets.QVBoxLayout(window.main_widget)

        # Graphs
        charge_time_plot = Canvas(window.main_widget)
        toolbar = NavigationToolbar(charge_time_plot, window, coordinates=False)
        StorageUse.charge_time_plot(selected_data, charge_time_plot)
        v_box.addWidget(toolbar)
        v_box.addWidget(charge_time_plot)

        # Table

        table_data = []
        for i in range(len(selected_data)):
            stats = StorageUse.charge_stats(selected_data[i])
            for j in range(len(stats[0])):
                if j == 0:
                    current_data = [selected_data[i].controllerName, j+1, "%.0f" % stats[0][j], "%.0f" % stats[1][j],
                                    "%.0f" % stats[2][j]]
                else:
                    current_data = ['---', j+1, "%.0f" % stats[0][j], "%.0f" % stats[1][j],
                                    "%.0f" % stats[2][j]]
                table_data.append(current_data)

        headers = ['Controller Name', 'Storage No.', 'Time Charging (s)', 'Time Discharging (s)', 'Time Idle (s)']
        tm = DataTableModel(table_data, headers, self.main_widget)
        tv = QtWidgets.QTableView()
        tv.setModel(tm)
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)
        vh = tv.verticalHeader()
        vh.setVisible(False)
        v_box.addWidget(tv)
        tv.setColumnWidth(0, 100)
        tv.setColumnWidth(1, 80)
        tv.setColumnWidth(2, 100)
        tv.setColumnWidth(3, 120)
        tv.setColumnWidth(4, 100)

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

    def file_quit(self):
        self.close()

    def closeEvent(self, ce):
        self.file_quit()

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

        selected_data = []
        if not selected:
            selected_data = [self.data_list[0]]
        else:
            for i in range(len(self.data_list)):
                if i in selected:
                    selected_data.append(self.data_list[i])

        return selected_data
