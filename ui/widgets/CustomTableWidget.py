from PyQt4 import QtCore, QtGui

class CustomTableWidget(QtGui.QTableWidget):

    keyPressed = QtCore.pyqtSignal('QKeyEvent')

    def __init__(self, parent = 0):
        QtGui.QTableWidget.__init__(self, parent)

    def keyPressEvent(self, event):
        self.keyPressed.emit(event)
        return QtGui.QTableWidget.keyPressEvent(self, event)
