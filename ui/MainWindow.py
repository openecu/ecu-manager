from PyQt4 import QtCore, QtGui
from PyQt4 import uic

from ui.dialogs.SettingsDialog import SettingsDialog
from ui.dialogs.AboutDialog import AboutDialog
from ui.widgets.TableViewWidget import TableViewWidget
from ui.widgets.SurfaceViewWidget import SurfaceViewWidget

from core.com.Connection import Connection

class MainWindow(QtGui.QMainWindow):

	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui = uic.loadUi('ui/resources/main_window.ui', self)

		self.ui.actionExit.triggered.connect(QtCore.QCoreApplication.instance().quit)
		self.ui.actionSettings.triggered.connect(self.settings_dialog)
		self.ui.actionAbout.triggered.connect(self.about_dialog)
		self.ui.tableViewButton.clicked.connect(self.table_view_dialog)
		self.ui.connectButton.clicked.connect(self.connect)

	def settings_dialog(self):
		settingsDialog = SettingsDialog()
		settingsDialog.exec_()

	def about_dialog(self):
		aboutDialog = AboutDialog(self)
		aboutDialog.exec_()

	def table_view_dialog(self):
		tableViewWidget = TableViewWidget()
		tableViewWidget.show()

	def connect(self):
		conn = Connection('COM4', 9600)
		conn.connect()
		conn.dataReceived.connect(self.update_sensors)

	def update_sensors(self, data):
		print(data)
