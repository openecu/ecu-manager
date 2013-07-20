from serial import Serial, SerialException
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

        self.initUi()

        self.update_ports()
        self.load_settings()

    def initUi(self):
        self.ui = uic.loadUi('ui/resources/settings_dialog.ui', self)

        self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.save_settings)
        self.ui.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.close)        
        self.ui.updateButton.clicked.connect(self.update_ports)
        self.ui.testButton.clicked.connect(self.test_connection)

    def save_settings(self):
        """Save settings"""

        settings.beginGroup('Connection')
        settings.setValue('PortName', self.ui.portNameComboBox.currentText())
        settings.setValue('BaudRate', self.ui.baudRateComboBox.currentText())
        settings.endGroup()

        self.close()

    def load_settings(self):
        """Load previously stored settings"""

        settings.beginGroup('Connection')
        port_name = settings.value('PortName')
        baud_rate = settings.value('BaudRate')
        settings.endGroup()

        for i in range(self.ui.portNameComboBox.count()):
            if self.ui.portNameComboBox.itemText(i) == port_name:
                self.ui.portNameComboBox.setCurrentIndex(i)

        for i in range(self.ui.baudRateComboBox.count()):
            if self.ui.baudRateComboBox.itemText(i) == baud_rate:
                self.ui.baudRateComboBox.setCurrentIndex(i)

    def update_ports(self):
        """Update COM ports list"""

        port_name = self.ui.portNameComboBox.currentText()
        self.ui.portNameComboBox.clear()

        for index, port in enumerate(list_ports.comports()):
            self.ui.portNameComboBox.addItem(port[0])

            if port_name == port[0]:
                self.ui.portNameComboBox.setCurrentIndex(index)

    def test_connection(self):
        """Test connection with defined settings"""

        port_name = self.ui.portNameComboBox.currentText()
        
        try:
            baud_rate = int(self.ui.baudRateComboBox.currentText())
        except ValueError:
            baud_rate = 9600    

        if not port_name or not baud_rate:
            QtGui.QMessageBox.warning(self, 'Test Connection', 'Please specify Port Name and Baud Rate')
        else:
            connected = False

            try:
                serial = Serial(port_name, baud_rate)

                if serial.isOpen():
                    connected = True
                    serial.close()
            except SerialException:
                pass

            if connected:
                QtGui.QMessageBox.information(self, 'Test Connection', 'Connection ok!')
            else:
                QtGui.QMessageBox.information(self, 'Test Connection', 'Connection failed!')
