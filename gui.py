from __future__ import unicode_literals
from voltage_frequency import *
from renewables import *
from running_cost import *
from storage_use import *
from generation_rejection import *
from data import *
from gui_backend import *
from PyQt5.QtWidgets import *

# This file handles all elements of the GUI. The MainWindow class has methods that setup the dashboard UI and each of
# the metric's UI.

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
        # Check if data is properly loaded
        if not self.data_list:
            self.statusBar().showMessage("No data loaded.", 1000)
            return

        selected_data = self.get_selected()

        unstable = False
        for i in range(len(selected_data)):
            if not selected_data[i].check_vf():
                unstable = True
                break

        if unstable:
            self.warning()

        else:
            # Data is properly loaded. Set up the UI.
            window = NewWindow(parent=self, title='Voltage and Frequency')
            window.setMinimumSize(1080, 700)

            # Layout
            v_box = QtWidgets.QVBoxLayout(window.main_widget)
            h_box = QtWidgets.QHBoxLayout(window.main_widget)
            v_box_left = QtWidgets.QVBoxLayout(window.main_widget)
            v_box_right = QtWidgets.QVBoxLayout(window.main_widget)
            toolbar_layout = QtWidgets.QHBoxLayout(window.main_widget)

            # Histogram width
            width = 0.6/len(selected_data)

            # Canvas setup
            hist_left = Canvas(window.main_widget)
            hist_left.fig.set_facecolor('lightsteelblue')
            time_plot_left = Canvas(window.main_widget)
            hist_right = Canvas(window.main_widget)
            time_plot_right = Canvas(window.main_widget)
            graph_list = [hist_left, hist_right, time_plot_left, time_plot_right]
            toolbar = NavigationToolbar(hist_left, window, coordinates=False)
            toolbar_layout.addWidget(toolbar)

            # VOLTAGE
            # Graphs
            VoltageAndFrequency.voltage_hist(selected_data, hist_left, 0, width)
            VoltageAndFrequency.voltage_time_plot(selected_data, time_plot_left, 0)
            v_box_left.addWidget(hist_left)
            bin_edit_left = QHBoxLayout(window.main_widget)
            edit_left = []

            def update_left_bins():
                hist_left.axes.clear()
                try:
                    lower = float(edit_left[0].text())
                    middle_left = float(edit_left[1].text())
                    middle_right = float(edit_left[2].text())
                    upper = float(edit_left[3].text())
                except ValueError:
                    VoltageAndFrequency.voltage_hist(selected_data, hist_left, bus_current, width)
                else:
                    VoltageAndFrequency.voltage_hist(selected_data, hist_left, bus_current, width,
                                                     lower, middle_left, middle_right, upper)
                hist_left.draw()

            for i in range(4):
                edit_left.append(QLineEdit(window.main_widget))
                edit_left[i].setMaximumWidth(80)
                edit_left[i].setMaximumHeight(25)
                bin_edit_left.addWidget(edit_left[i])

            bin_apply_left = QPushButton('Apply', window.main_widget)
            bin_apply_left.setMaximumWidth(80)
            bin_apply_left.setMaximumHeight(80)
            bin_apply_left.clicked.connect(update_left_bins)
            bin_edit_left.addWidget(bin_apply_left)

            v_box_left.addLayout(bin_edit_left)
            v_box_left.addWidget(time_plot_left)

            # Table
            headers = ['Controller Name', 'Std. Deviation', 'Mean']
            table_data_left = []
            for i in range(len(selected_data)):
                stats = VoltageAndFrequency.voltage_stats(selected_data[i], 0)
                current_data = [selected_data[i].controllerName, "%.2f" % stats[0], "%.2f" % stats[1]]
                table_data_left.append(current_data)

            tm_left = DataTableModel(table_data_left, headers, window.main_widget)
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
            VoltageAndFrequency.frequency_hist(selected_data, hist_right, 0, width)
            VoltageAndFrequency.frequency_time_plot(selected_data, time_plot_right, 0)
            v_box_right.addWidget(hist_right)

            bin_edit_right = QHBoxLayout(window.main_widget)
            edit_right = []

            def update_right_bins():
                hist_right.axes.clear()
                try:
                    lower = float(edit_right[0].text())
                    middle_left = float(edit_right[1].text())
                    middle_right = float(edit_right[2].text())
                    upper = float(edit_right[3].text())
                except ValueError:
                    VoltageAndFrequency.frequency_hist(selected_data, hist_right, bus_current, width)
                else:
                    VoltageAndFrequency.frequency_hist(selected_data, hist_right, bus_current, width,
                                                     lower, middle_left, middle_right, upper)
                hist_right.draw()

            for i in range(4):
                edit_right.append(QLineEdit(window.main_widget))
                edit_right[i].setMaximumWidth(80)
                edit_right[i].setMaximumHeight(25)
                bin_edit_right.addWidget(edit_right[i])

            bin_apply_right = QPushButton('Apply', window.main_widget)
            bin_apply_right.setMaximumWidth(80)
            bin_apply_right.setMaximumHeight(80)
            bin_apply_right.clicked.connect(update_right_bins)
            bin_edit_right.addWidget(bin_apply_right)
            v_box_right.addLayout(bin_edit_right)

            v_box_right.addWidget(time_plot_right)

            # Table
            headers = ['Controller Name', 'Std. Deviation', 'Mean']
            table_data_right = []
            for i in range(len(selected_data)):
                stats = VoltageAndFrequency.frequency_stats(selected_data[i], 0)
                current_data = [selected_data[i].controllerName, "%.2f" % stats[0], "%.2f" % stats[1]]
                table_data_right.append(current_data)

            tm_right = DataTableModel(table_data_right, headers, window.main_widget)
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

            # Toolbar switching
            def update_hist_left(event):
                hist_left.set_toolbar_active(graph_list, toolbar)

            def update_hist_right(event):
                hist_right.set_toolbar_active(graph_list, toolbar)

            def update_time_plot_left(event):
                time_plot_left.set_toolbar_active(graph_list, toolbar)

            def update_time_plot_right(event):
                time_plot_right.set_toolbar_active(graph_list, toolbar)

            time_plot_right.mouseDoubleClickEvent = update_time_plot_right
            hist_right.mouseDoubleClickEvent = update_hist_right
            time_plot_left.mouseDoubleClickEvent = update_time_plot_left
            hist_left.mouseDoubleClickEvent = update_hist_left
            canvas_list = [time_plot_right, time_plot_left, hist_right, hist_left]

            # Bus switching
            n_bus = []
            for i in range(len(selected_data)):
                n_bus.append(selected_data[i].nBus)
            n_bus = min(n_bus)
            bus_current = 0

            def switch_bus():
                nonlocal bus_current
                if n_bus < 2:
                    return
                if bus_current < (n_bus - 1):
                    bus_current += 1
                else:
                    bus_current = 0
                for j in range(0, len(canvas_list)):
                    canvas_list[j].axes.clear()
                VoltageAndFrequency.voltage_time_plot(selected_data, time_plot_left, bus_current)
                VoltageAndFrequency.frequency_time_plot(selected_data, time_plot_right, bus_current)
                label = "Bus: " + ("%d" % (bus_current + 1))
                bus_label.setText(label)
                for j in range(0, len(canvas_list)):
                    canvas_list[j].draw()

                nonlocal table_data_right, table_data_left, tv_right, tv_left
                table_data_right, table_data_left = [], []
                for i in range(len(selected_data)):
                    stats = VoltageAndFrequency.voltage_stats(selected_data[i], bus_current)
                    current_data = [selected_data[i].controllerName, "%.2f" % stats[0], "%.2f" % stats[1]]
                    table_data_left.append(current_data)
                    stats = VoltageAndFrequency.frequency_stats(selected_data[i], bus_current)
                    current_data = [selected_data[i].controllerName, "%.2f" % stats[0], "%.2f" % stats[1]]
                    table_data_right.append(current_data)
                tm = DataTableModel(table_data_left, headers, self.main_widget)
                tv_left.setModel(tm)
                tm = DataTableModel(table_data_right, headers, self.main_widget)
                tv_right.setModel(tm)

                update_left_bins()
                update_right_bins()

            bus_button = QtWidgets.QPushButton('Next Bus', window.main_widget)
            bus_button.setFixedSize(150, 20)
            bus_button.clicked.connect(switch_bus)
            bus_label = QtWidgets.QLabel('Bus: 1', window.main_widget)
            toolbar_layout.addStretch()
            toolbar_layout.addWidget(bus_button)
            toolbar_layout.addWidget(bus_label)

            # Layout finalization
            v_box.addLayout(toolbar_layout)
            v_box.addLayout(h_box)
            h_box.addLayout(v_box_left)
            h_box.addLayout(v_box_right)

    def gr(self):
        if not self.data_list:
            self.statusBar().showMessage("No data loaded.", 1000)
            return

        selected_data = self.get_selected()

        unstable = False
        for i in range(len(selected_data)):
            if not selected_data[i].check_gr():
                unstable = True
                break

        if unstable:
            self.warning()

        else:

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
            tm = DataTableModel(table_data, headers, window.main_widget)
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

        unstable = False
        for i in range(len(selected_data)):
            if not selected_data[i].check_rei():
                unstable = True
                break

        if unstable:
            self.warning()

        else:

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
                Renewables.renewable_pie(selected_data[i], canvas_list[i])
                pie_box.addWidget(canvas_list[i])

            # Normalize pie chart button
            norm_button = QtWidgets.QPushButton('Normalize Pie Chart', window)
            norm_button.setCheckable(True)
            norm_button.setFixedSize(150, 20)

            def switch_pie():
                    if norm_button.isChecked():
                        for j in range(n_pies):
                            canvas_list[j].axes.clear()
                            Renewables.renewable_norm_pie(selected_data[j], canvas_list[j])
                            canvas_list[j].draw()
                    else:
                        for j in range(n_pies):
                            canvas_list[j].axes.clear()
                            Renewables.renewable_pie(selected_data[j], canvas_list[j])
                            canvas_list[j].draw()

            norm_button.clicked.connect(switch_pie)

            # Table
            table_data = []
            num_gen = 0
            for i in range(len(selected_data)):
                num_gen, stats, headers = Renewables.renewable_stats(selected_data[i])
                current_data = stats
                current_data.insert(0, selected_data[i].controllerName)
                table_data.append(current_data)

            headers.insert(0, 'Controller Name')

            tm = DataTableModel(table_data, headers, window.main_widget)
            tv = QtWidgets.QTableView()
            tv.setModel(tm)
            hh = tv.horizontalHeader()
            hh.setStretchLastSection(True)
            vh = tv.verticalHeader()
            vh.setVisible(False)
            table_box.addWidget(tv)
            tv.setColumnWidth(0, 100)
            for i in range(1, num_gen-1):
                tv.setColumnWidth(i, 75)
            tv.setColumnWidth(num_gen-1, 100)

            v_box.addLayout(pie_box)
            v_box.addWidget(norm_button)
            v_box.addLayout(table_box)

    def rc(self):
        if not self.data_list:
            self.statusBar().showMessage("No data loaded.", 1000)
            return

        selected_data = self.get_selected()

        unstable = False
        for i in range(len(selected_data)):
            if not selected_data[i].check_rc():
                unstable = True
                break

        if unstable:
            self.warning()

        else:

            window = NewWindow(parent=self, title='Running Costs')
            window.setMinimumSize(750, 950)

            # Layout
            v_box = QtWidgets.QVBoxLayout(window.main_widget)
            switch_table_box = QtWidgets.QHBoxLayout(window.main_widget)
            stats_table_box = QtWidgets.QHBoxLayout(window.main_widget)
            toolbar_layout = QtWidgets.QHBoxLayout(window.main_widget)

            # Canvas setup
            pwr_out = Canvas(window.main_widget)
            fuel_use = Canvas(window.main_widget)
            toolbar = NavigationToolbar(pwr_out, window, coordinates=False)
            toolbar_layout.addWidget(toolbar)
            v_box.addLayout(toolbar_layout)

            fuel_types = RunningCost.basic_calc(selected_data)
            RunningCost.pwr_gen_time(selected_data, 0, pwr_out)
            RunningCost.fuel_use(selected_data, 0, fuel_use)

            v_box.addWidget(pwr_out)
            v_box.addWidget(fuel_use)
            graph_list = [pwr_out, fuel_use]

            # Toolbar switching setup
            def update_hist(event):
                pwr_out.set_toolbar_active(graph_list, toolbar)

            def update_time_plot(event):
                fuel_use.set_toolbar_active(graph_list, toolbar)

            pwr_out.mouseDoubleClickEvent = update_hist
            fuel_use.mouseDoubleClickEvent = update_time_plot
            pwr_out.fig.set_facecolor('lightsteelblue')

            # Button for rotating between fuel types
            button_list = []
            button_list.insert(0, 'Total Fuel')
            for each in fuel_types:
                button_list.append(each)
            type = 0

            def switch_fuel_type():
                nonlocal type
                if type < (len(button_list)-1):
                    type += 1
                else:
                    type = 0

                pwr_out.axes.clear()
                fuel_use.axes.clear()
                RunningCost.pwr_gen_time(selected_data, type, pwr_out)
                RunningCost.fuel_use(selected_data, type, fuel_use)
                label = button_list[type]
                fuel_label.setText(label)
                pwr_out.draw()
                fuel_use.draw()

            # todo: include variable table data if needed

            fuel_button = QtWidgets.QPushButton('Change Fuel Type', window.main_widget)
            fuel_button.setFixedSize(150, 20)
            fuel_button.clicked.connect(switch_fuel_type)
            fuel_label = QtWidgets.QLabel('Total Fuel', window.main_widget)
            toolbar_layout.addStretch()
            toolbar_layout.addWidget(fuel_button)
            toolbar_layout.addWidget(fuel_label)

            # Stats Table
            tl = QtWidgets.QLabel("Stats affecting Running Cost \n", window.main_widget)
            font = QtGui.QFont()
            font.setBold(True)
            tl.setFont(font)
            stats_table_box.addWidget(tl)
            headers = ['Controller Name', 'Fuel Consumption(L)', 'Average Ramping\n(MW/s)', 'Max Ramping\n(MW/s)',
                       'Peak Power\n(Grid Connected) (MW)']
            RunningCost.ramping(selected_data)
            table_data = RunningCost.rc_stats(selected_data)

            for i in range(len(selected_data)):
                table_data[i].insert(0, selected_data[i].controllerName)

            tm = DataTableModel(table_data, headers, self.main_widget)
            tv = QtWidgets.QTableView()
            tv.setModel(tm)
            hh = tv.horizontalHeader()
            hh.setStretchLastSection(True)
            vh = tv.verticalHeader()
            vh.setVisible(False)
            v_box.addLayout(stats_table_box)
            v_box.addWidget(tv)
            tv.setColumnWidth(0, 100)
            tv.setColumnWidth(1, 120)
            tv.setColumnWidth(2, 120)
            tv.setColumnWidth(3, 120)
            tv.setColumnWidth(4, 120)

            # Switch count Table
            tl1 = QtWidgets.QLabel("Occurrences of On/Off Switching per DER \n", window.main_widget)
            font = QtGui.QFont()
            font.setBold(True)
            tl1.setFont(font)
            switch_table_box.addWidget(tl1)
            tl2 = QtWidgets.QLabel("If 'Fuel': off: consumption = 0 \n"
                                   "If 'Renewable': off: generation < 5% Cacpacity", window.main_widget)
            switch_table_box.addWidget(tl2)

            headers = ['Controller Name']
            for i in range(selected_data[0].nDer):
                headers.append(selected_data[0].derList[i].energy_type)

            table_data = RunningCost.switching(selected_data)

            for i in range(len(selected_data)):
                table_data[i].insert(0, selected_data[i].controllerName)

            tm = DataTableModel(table_data, headers, self.main_widget)
            tv = QtWidgets.QTableView()
            tv.setModel(tm)
            hh = tv.horizontalHeader()
            hh.setStretchLastSection(True)
            vh = tv.verticalHeader()
            vh.setVisible(False)
            v_box.addLayout(switch_table_box)
            v_box.addWidget(tv)
            tv.setColumnWidth(0, 100)
            for i in range(1, len(headers)):
                tv.setColumnWidth(i, 70)

            v_box.addLayout(switch_table_box)

    def su(self):
        if not self.data_list:
            self.statusBar().showMessage("No data loaded.", 1000)
            return

        selected_data = self.get_selected()

        unstable = False
        for i in range(len(selected_data)):
            if not selected_data[i].check_su():
                unstable = True
                break

        if unstable:
            self.warning()

        else:
            storage_use = StorageUse(selected_data)
            window = NewWindow(parent=self, title='Storage Use')
            window.setMinimumSize(650, 750)

            # Layout
            v_box = QtWidgets.QVBoxLayout(window.main_widget)
            toolbar_layout = QtWidgets.QHBoxLayout(window.main_widget)

            # Histogram width
            width = 0.6 / len(selected_data)

            # Graphs
            charge_hist = Canvas(window.main_widget)
            charge_time_plot = Canvas(window.main_widget)
            toolbar = NavigationToolbar(charge_hist, window, coordinates=False)
            toolbar_layout.addWidget(toolbar)
            v_box.addLayout(toolbar_layout)
            storage_use.charge_hist(selected_data, charge_hist, width)
            storage_use.charge_time_plot(selected_data, charge_time_plot)

            bin_edit = QHBoxLayout(window.main_widget)
            edit = []

            def update_bins():
                charge_hist.axes.clear()
                try:
                    lower = int(edit[0].text())
                    middle_left = int(edit[1].text())
                    middle_right = int(edit[2].text())
                    upper = int(edit[3].text())
                except ValueError:
                    storage_use.charge_hist(selected_data, charge_hist, width)
                else:
                    storage_use.charge_hist(selected_data, charge_hist, width,
                                                       lower, middle_left, middle_right, upper)
                charge_hist.draw()

            for i in range(4):
                edit.append(QLineEdit(window.main_widget))
                edit[i].setMaximumWidth(80)
                edit[i].setMaximumHeight(25)
                bin_edit.addWidget(edit[i])

            bin_apply = QPushButton('Apply', window.main_widget)
            bin_apply.setMaximumWidth(80)
            bin_apply.setMaximumHeight(80)
            bin_apply.clicked.connect(update_bins)
            bin_edit.addWidget(bin_apply)

            v_box.addWidget(charge_hist)
            v_box.addLayout(bin_edit)
            v_box.addWidget(charge_time_plot)

            graph_list = [charge_hist, charge_time_plot]

            # Toolbar switching setup
            def update_hist(event):
                charge_hist.set_toolbar_active(graph_list, toolbar)

            def update_time_plot(event):
                charge_time_plot.set_toolbar_active(graph_list, toolbar)

            charge_hist.mouseDoubleClickEvent = update_hist
            charge_time_plot.mouseDoubleClickEvent = update_time_plot
            charge_hist.fig.set_facecolor('lightsteelblue')

            # Table
            table_data = []
            for i in range(len(selected_data)):
                stats = storage_use.charge_stats(selected_data)
                current_data = [selected_data[i].controllerName, "%.0f" % stats[0][i], "%.0f" % stats[1][i],
                                "%.0f" % stats[2][i]]
                table_data.append(current_data)

            # Storage switching

            def switch_storage():
                label = 'Storage: ' + str(storage_use.next_storage() + 1)
                storage_label.setText(label)
                charge_time_plot.axes.clear()
                charge_hist.axes.clear()
                storage_use.charge_time_plot(selected_data, charge_time_plot)
                charge_time_plot.draw()
                charge_hist.draw()
                table_data = []
                for i in range(len(selected_data)):
                    stats = storage_use.charge_stats(selected_data)
                    current_data = [selected_data[i].controllerName, "%.0f" % stats[0][i], "%.0f" % stats[1][i],
                                    "%.0f" % stats[2][i]]
                    table_data.append(current_data)
                tm = DataTableModel(table_data, headers, window.main_widget)
                tv.setModel(tm)

                update_bins()

            storage_button = QtWidgets.QPushButton('Next Storage', window.main_widget)
            storage_button.setFixedSize(150, 20)
            storage_button.clicked.connect(switch_storage)
            storage_label = QtWidgets.QLabel('Storage: 1', window.main_widget)
            toolbar_layout.addStretch()
            toolbar_layout.addWidget(storage_button)
            toolbar_layout.addWidget(storage_label)

            headers = ['Controller Name', 'Time Charging (s)', 'Time Discharging (s)', 'Time Idle (s)']
            tm = DataTableModel(table_data, headers, window.main_widget)
            tv = QtWidgets.QTableView()
            tv.setModel(tm)
            hh = tv.horizontalHeader()
            hh.setStretchLastSection(True)
            vh = tv.verticalHeader()
            vh.setVisible(False)
            v_box.addWidget(tv)
            tv.setColumnWidth(0, 100)
            tv.setColumnWidth(1, 120)
            tv.setColumnWidth(2, 120)
            tv.setColumnWidth(3, 120)

    def open_file(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '*.mat; *.txt')
        if filename[0] == '':
            return
        try:
            self.data_list.append(Data(filename[0]))
        except:
            self.data_warning()
            return
        else:
            if not self.data_list[-1].done_flag:
                self.sort_data()
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

    def warning(self):
        error = QMessageBox.warning(self, "Error", "Data missing in at least 1 sample. \nCheck data for errors",
                                    QMessageBox.Ok)

    def data_warning(self):
        error = QMessageBox.critical(self, "Error", "Incompatible data formatting", QMessageBox.Ok)

    def sort_data(self):
        window = NewWindow(parent=self, title='Data Sorter')
        window.setMinimumSize(500, 700)
        v_box = QtWidgets.QVBoxLayout(window.main_widget)
        table_data = self.data_list[-1].temp_label_list
        tv = QtWidgets.QTableWidget(len(table_data), 2, window.main_widget)
        v_box.addWidget(tv)
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)
        vh = tv.verticalHeader()
        vh.setVisible(False)
        tv.setColumnWidth(0, 150)
        tv.setHorizontalHeaderLabels(['Variable Name', 'Label'])
        line_edit_list = []
        for i in range(len(table_data)):
            tv.setItem(i, 0, QTableWidgetItem(table_data[i]))
            line_edit_list.append(QLineEdit(window.main_widget))
            tv.setCellWidget(i, 1, line_edit_list[i])

        h_box = QHBoxLayout(window.main_widget)
        controller_prompt = QLabel("Enter controller/data set name: ")
        controller_name_edit = QLineEdit(window.main_widget)
        controller_name_edit.setMaximumWidth(200)
        h_box.addWidget(controller_prompt)
        h_box.addWidget(controller_name_edit)
        h_box.addStretch()
        v_box.addLayout(h_box)

        description = QLabel( "TIME (T)\n\n"
                              "BUS\n"
                              "Voltage (V-bus#-unit) e.g. (V-bus1-pu)\n"
                              "Frequency (F-bus#-unit) e.g. (F-bus1-Hz)\n\n"
                              "DER\n"
                              "Power Output (Po-der#-type-capacity-unit) e.g. (Po-der1-Fuel_Hydro-1000-kW)\n"
                              "Consumption (C-der#-unit) e.g. (C-der1-L)\n"
                              "State of Charge (SOC-der#) e.g (SOC-der1)\n\n"
                              "LOAD\n"
                              "Power Demand (Pd-load#-type-unit) e.g. (Pd-load1-Priority-kW)")
        v_box.addWidget(description)

        def assign_labels():
            temp_label_list = []
            k = 0
            for i in range(len(self.data_list[-1].temp_index)):
                current_list = []
                for j in self.data_list[-1].temp_index[i]:
                    current_list.append(line_edit_list[k].text())
                    k += 1
                temp_label_list.append(current_list)

            self.data_list[-1].temp_label_list = temp_label_list
            self.data_list[-1].controllerName = controller_name_edit.text()
            print(temp_label_list)
            window.close()
            self.data_list[-1].sort_labelled_data()
            self.update_table()

        done_button = QPushButton('Done')
        done_button.setMaximumWidth(120)
        done_button.clicked.connect(assign_labels)
        v_box.addWidget(done_button)
