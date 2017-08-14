from PyQt5 import QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# This file contains misc. classes that are often called in gui.py


# Class used to contain graphs as widget in the PyQt 5 framework
class Canvas(FigureCanvas):
    def __init__(self, parent=None, width=4, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.axes = self.fig.add_subplot(111)

    def set_toolbar_active(self, graph_list, toolbar):
        if not toolbar.canvas == self:
            toolbar.canvas = self
            toolbar.dynamic_update()
            for i in range(len(graph_list)):
                graph_list[i].fig.set_facecolor('white')
                graph_list[i].draw()
            self.fig.set_facecolor('lightsteelblue')
        else:
            return


# Class used to setup a new separate window
class NewWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, title='New Window'):
        super(NewWindow, self).__init__(parent)
        self.setMinimumSize(400, 400)
        self.move(0, 210)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.main_widget = QtWidgets.QWidget(self)
        self.setWindowTitle(title)
        self.show()
        self.setCentralWidget(self.main_widget)


# Model for a table used to display information
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