import numpy
from scipy.interpolate import interp1d, interp2d

from PyQt4 import QtGui
from PyQt4 import uic

class TableViewWidget(QtGui.QWidget):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.initUi()
        self.init_data()
        self.update()

    def initUi(self):
        self.ui = uic.loadUi('ui/resources/table_view_widget.ui', self)

        self.ui.tableWidget.setRowCount(16)
        self.ui.tableWidget.setColumnCount(16)
        self.ui.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        self.ui.tableWidget.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)

        self.ui.tableWidget.cellChanged.connect(self.cell_edit)
        self.ui.interpButton.clicked.connect(self.interp_data)
        self.ui.filterButton.clicked.connect(self.filter_data)
        self.ui.clearButton.clicked.connect(self.clear_data)

    def init_data(self):
        self.data = [[0 for i in range(16)] for j in range(16)]

    def interp_data(self):
        if len(self.ui.tableWidget.selectedRanges()) > 0:
            sel = self.ui.tableWidget.selectedRanges()[0]

            rc = sel.rowCount()
            cc = sel.columnCount()

            x = sel.leftColumn();
            _x = sel.rightColumn()
            y = sel.topRow()
            _y = sel.bottomRow()
            _z = [[self.data[y][x], self.data[y][_x]], [self.data[_y][x], self.data[_y][_x]]]
            z = numpy.array(_z)

            if rc == 1 and cc > 1:
                _z = interp1d([x, _x], z[0])(range(x, _x + 1))
                for i in range(0, sel.columnCount()):
                    self.data[y][x + i] = _z[i]

            elif cc == 1 and rc > 1:
                _z = interp1d([y, _y], [z[0][0], z[1][0]])(range(y, _y + 1))
                for i in range(0, sel.rowCount()):
                    self.data[y + i][x] = _z[i]

            elif rc > 1 and cc > 1:
                _z = interp2d([x, _x], [y, _y], z)(range(x, _x + 1), range(y, _y + 1))
                for i in range(0, sel.columnCount()):
                    for j in range(0, sel.rowCount()):
                        self.data[y + j][x + i] = _z[j][i]

        self.update()        

    def filter_data(self):
        pass

    def clear_data(self):
        for i in range(16):
            for j in range(16):
                self.data[j][i] = 0   

        self.update()     

    def update(self):
        QtGui.QWidget.update(self)

        for i in range(16):
            for j in range(16):
                self.ui.tableWidget.setItem(i, j, QtGui.QTableWidgetItem('%.2f' % self.data[i][j]))
                g = int(255 - self.data[i][j] / 1 * 96)
                self.ui.tableWidget.item(i, j).setBackground(QtGui.QColor(255, g, 128))

    def cell_edit(self, x, y):
        try:
            value = float(self.ui.tableWidget.item(x, y).text())
        except ValueError:
            value = 0

        self.data[x][y] = value
        self.ui.tableWidget.item(x, y).setText('%.2f' % value)
