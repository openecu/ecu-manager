from PyQt4 import QtCore, QtGui
from PyQt4 import uic

from ui.dialogs.SettingsDialog import SettingsDialog
from ui.dialogs.AboutDialog import AboutDialog
from ui.widgets.TableViewWidget import TableViewWidget
from ui.widgets.SurfaceViewWidget import SurfaceViewWidget

from app.App import App
from core.com.Connection import Connection, Protocol

class MainWindow(QtGui.QMainWindow):

	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.app = App.instance()
		self.ui = uic.loadUi('ui/resources/main_window.ui', self)

		self.ui.setWindowTitle(self.app.applicationName())

		self.ui.treeWidget.header().setStretchLastSection(False)
		self.ui.treeWidget.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
		self.ui.treeWidget.expandAll()

		test_data = [
			['Base', [
				['RPM', ''],
				['Load', 'mg'],
				['A/F Ratio', ''],
			]],
			['Injection', [
				['Pulse width', 'ms'], 
				['Target A/F Ratio', ''], 
				['Timing', '°'],
			]],
			['Ignition', [
				['Timing Advance', '°BTDC'],
				['Dwell Time', 'ms'],
			]],
			['Idle', [
				['Target RPM', ''],
				['Delta RPM', ''],
				['Timing Advance', '°BTDC'],
				['Timing Offset', '°'],
				['PWM Duty', '%'],
			]],
		]
		column_count = 0
		for i in range(len(test_data)):
			column_count += 1 + len(test_data[i][1])

		self.ui.paramsTableWidget.setColumnCount(3)
		self.ui.paramsTableWidget.setRowCount(column_count)
		self.ui.paramsTableWidget.horizontalHeader().resizeSection(0, 123)
		self.ui.paramsTableWidget.horizontalHeader().resizeSection(1, 50)
		self.ui.paramsTableWidget.horizontalHeader().resizeSection(2, 55)

		row_index = 0

		for group in test_data:
			self.ui.paramsTableWidget.setSpan(row_index, 0, 1, 3)
			self.ui.paramsTableWidget.setItem(row_index, 0, QtGui.QTableWidgetItem(group[0]))
			self.ui.paramsTableWidget.item(row_index, 0).setBackground(QtCore.Qt.darkGray)
			self.ui.paramsTableWidget.item(row_index, 0).setForeground(QtCore.Qt.white)
			row_index += 1

			for param in group[1]:
				self.ui.paramsTableWidget.setItem(row_index, 0, QtGui.QTableWidgetItem(param[0]))
				self.ui.paramsTableWidget.setItem(row_index, 2, QtGui.QTableWidgetItem(param[1]))
				row_index += 1

		self.ui.actionExit.triggered.connect(QtCore.QCoreApplication.instance().quit)
		self.ui.actionSettings.triggered.connect(self.settings_dialog)
		self.ui.actionAbout.triggered.connect(self.about_dialog)
		self.ui.actionAbout_Qt.triggered.connect(QtGui.QApplication.aboutQt)
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
		conn = Connection('COM4', 9600, Protocol())
		conn.connect()
		conn.packetReceived.connect(self.update_sensors)

	def update_sensors(self, packet):
		print(packet.data)
