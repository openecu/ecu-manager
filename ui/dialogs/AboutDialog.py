from PyQt4 import QtCore, QtGui
from PyQt4 import uic

class AboutDialog(QtGui.QDialog):

	def __init__(self):
		QtGui.QDialog.__init__(self)
		self.ui = uic.loadUi('ui/resources/about_dialog.ui', self)
