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

class Packet(object):

    size = 0
    data = list()

    def __init__(self, data):
        self.data = data

class Protocol(object):

    WAIT = 0
    READ_SIZE = 2
    READ_DATA = 3

    def __init__(self):
        self.state = Protocol.WAIT

    def parse_data(self, data):
        for b in data:
            if self.state == Protocol.WAIT:
                if b == 0xFF:
                    self.state = Protocol.READ_SIZE
                    self.packet = Packet()
            elif self.state == Protocol.READ_SIZE:
                pass
            elif self.state == Protocol.READ_DATA:
                pass

    def is_ready(self):
        pass

    def get_packet(self):
        pass

class Connection(QtCore.QObject):
    """
    Connection
    """

    packetReceived = QtCore.pyqtSignal(object)
    connected = False

    def __init__(self, port_name, baud_rate, proto):
        QtCore.QObject.__init__(self)

        self.port_name = port_name
        self.baud_rate = baud_rate
        self.proto = proto

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
        self.proto.parse_data(data)

        if self.proto.is_ready():
            self.packetReceived.emit(self.proto.get_packet())
