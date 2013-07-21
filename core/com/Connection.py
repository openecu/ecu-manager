from serial import Serial, SerialException
import threading

from PyQt4 import QtCore

class ReadThread(threading.Thread):
    """Serial port read thread"""

    def __init__(self, serial, received):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.serial = serial
        self.received = received

    def run(self):
        """Thread loop"""

        while 1:
            if self.serial.isOpen():
                data = self.serial.read(1)
                n = self.serial.inWaiting()

                if n > 0:
                    data += self.serial.read(n)

                self.received(data)

class WriteThread(threading.Thread):
    """Serial port write thread"""

    def __init__(self, serial, sent):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.serial = serial
        self.sent = sent

    def run(self):
        """Thread loop"""
        pass

class Connection(QtCore.QObject):
    """
    Connection
    """

    dataReceived = QtCore.pyqtSignal(bytes)
    connected = False

    def __init__(self, port_name, baud_rate=9600):
        QtCore.QObject.__init__(self)

        self.port_name = port_name
        self.baud_rate = baud_rate
        self.serial = Serial()
        ReadThread(self.serial, self.dataReceivedEvent).start()

    def connect(self):
        """Connect"""

        self.serial.port = self.port_name
        self.serial.baudrate = self.baud_rate
        self.connected = False

        try:
            self.serial.open()

            if self.serial.isOpen():
                self.connected = True

        except SerialException:
            pass

    def disconnect(self):
        """Disconnect"""

        if self.serial.isOpen():
            self.serial.close()

    def is_connected(self):
        return self.connected

    def dataReceivedEvent(self, data):
        self.dataReceived.emit(data)
