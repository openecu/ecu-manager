from PyQt4 import QtCore, QtGui
from PyQt4 import uic

class SurfaceViewWidget(QtGui.QWidget):
    """
    Surface view widget
    """

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.initUi()

    def initUi(self):
        pass

