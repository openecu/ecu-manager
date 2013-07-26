import sys

from PyQt4.QtCore import QSettings

from ui.MainWindow import MainWindow
from app.App import App

def main():
    """Entry point function"""

    app = App(sys.argv)
    app.setApplicationName('ECU Manager')
    app.setSettings(QSettings('Community', 'ECU Manager'))

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
