from PyQt4 import QtCore, QtGui
from PyQt4 import uic

class AboutDialog(QtGui.QDialog):

	def __init__(self, parent = None):
		QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
		self.ui = uic.loadUi('ui/resources/about_dialog.ui', self)
