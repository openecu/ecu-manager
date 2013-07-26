from PyQt4.QtGui import QApplication 

class App(QApplication):

    _instance = None

    def __init__(self, argv):
        QApplication.__init__(self, argv)
        App._instance = self

    def instance():
        return App._instance

    def setSettings(self, settings):
        self._settings = settings

    def settings(self):
        return self._settings
