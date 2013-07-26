from serial import Serial, SerialException
from serial.tools import list_ports

from PyQt4.QtGui import QDialog, QDialogButtonBox, QMessageBox
from PyQt4 import uic

from app.App import App

class SettingsDialog(QDialog):
    """
    Application settings dialog
    """

    def __init__(self):
        QDialog.__init__(self)

        self.app = App.instance()
        self.settings = self.app.settings()
        self.initUi()

        self.updatePorts()
        self.loadSettings()

    def initUi(self):
        self.ui = uic.loadUi('ui/resources/settings_dialog.ui', self)

        self.ui.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.saveSettings)
        self.ui.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.close)        
        self.ui.updateButton.clicked.connect(self.updatePorts)
        self.ui.testButton.clicked.connect(self.testConnection)

    def saveSettings(self):
        """Save settings"""

        self.settings.beginGroup('Connection')
        self.settings.setValue('PortName', self.ui.portNameComboBox.currentText())
        self.settings.setValue('BaudRate', self.ui.baudRateComboBox.currentText())
        self.settings.endGroup()

        self.close()

    def loadSettings(self):
        """Load previously stored settings"""

        self.settings.beginGroup('Connection')
        port_name = self.settings.value('PortName')
        baud_rate = self.settings.value('BaudRate')
        self.settings.endGroup()

        for i in range(self.ui.portNameComboBox.count()):
            if self.ui.portNameComboBox.itemText(i) == port_name:
                self.ui.portNameComboBox.setCurrentIndex(i)

        for i in range(self.ui.baudRateComboBox.count()):
            if self.ui.baudRateComboBox.itemText(i) == baud_rate:
                self.ui.baudRateComboBox.setCurrentIndex(i)

    def updatePorts(self):
        """Update COM ports list"""

        port_name = self.ui.portNameComboBox.currentText()
        self.ui.portNameComboBox.clear()

        for index, port in enumerate(list_ports.comports()):
            self.ui.portNameComboBox.addItem(port[0])

            if port_name == port[0]:
                self.ui.portNameComboBox.setCurrentIndex(index)

    def testConnection(self):
        """Test connection with defined settings"""

        port_name = self.ui.portNameComboBox.currentText()
        
        try:
            baud_rate = int(self.ui.baudRateComboBox.currentText())
        except ValueError:
            baud_rate = 9600    

        if not port_name or not baud_rate:
            QMessageBox.warning(self, 'Test Connection', 'Please specify Port Name and Baud Rate')
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
                QMessageBox.information(self, 'Test Connection', 'Connection ok!')
            else:
                QMessageBox.information(self, 'Test Connection', 'Connection failed!')
