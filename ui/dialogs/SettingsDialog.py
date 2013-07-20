from serial.tools import list_ports

from PyQt4 import QtCore, QtGui
from PyQt4 import uic

from settings import settings

class SettingsDialog(QtGui.QDialog):
	"""
	Application settings dialog
	"""

	def __init__(self):
		QtGui.QDialog.__init__(self)
		self.ui = uic.loadUi('ui/resources/settings_dialog.ui', self)

		self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.save_settings)
		self.ui.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.close)

		self.update_ports()
		self.load_settings()

	def save_settings(self):
		"""Save settings"""

		settings.beginGroup('Connection')
		settings.setValue('PortName', self.ui.portNameComboBox.currentText())
		settings.setValue('BaudRate', self.ui.baudRateComboBox.currentText())
		settings.endGroup()

		self.close()

	def load_settings(self):
		"""Load previously stored settings"""

		port_name = settings.value('Connection/PortName')
		baud_rate = settings.value('Connection/BaudRate')

		for i in range(self.ui.portNameComboBox.count()):
			if self.ui.portNameComboBox.itemText(i) == port_name:
				self.ui.portNameComboBox.setCurrentIndex(i)

		for i in range(self.ui.baudRateComboBox.count()):
			if self.ui.baudRateComboBox.itemText(i) == baud_rate:
				self.ui.baudRateComboBox.setCurrentIndex(i)

	def update_ports(self):
		"""Update COM ports list"""

		for index, port in enumerate(list_ports.comports()):
			self.ui.portNameComboBox.addItem(port[0])
