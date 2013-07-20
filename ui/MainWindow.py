from PyQt4 import QtCore, QtGui
from PyQt4 import uic

from ui.dialogs.SettingsDialog import SettingsDialog
from ui.dialogs.AboutDialog import AboutDialog

class MainWindow(QtGui.QMainWindow):

	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui = uic.loadUi('ui/resources/main_window.ui', self)

		self.ui.actionExit.triggered.connect(QtCore.QCoreApplication.instance().quit)
		self.ui.actionSettings.triggered.connect(self.settings_dialog)
		self.ui.actionAbout.triggered.connect(self.about_dialog)

	def settings_dialog(self):
		settingsDialog = SettingsDialog()
		settingsDialog.exec_()

	def about_dialog(self):
		aboutDialog = AboutDialog()
		aboutDialog.exec_()
