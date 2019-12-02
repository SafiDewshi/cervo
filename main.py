from PyQt5 import uic, QtCore, QtGui, QtWidgets
import sys
import requests

Ui_MainWindow, QtBaseClass = uic.loadUiType("cervo.ui")


class CervoUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.searchButton.clicked.connect(self.search)

    def search(self):
        searchstring = self.searchBar.text()
        print(searchstring)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CervoUI()
    window.show()
    sys.exit(app.exec_())