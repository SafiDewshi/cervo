import cervoui
import requests
import sys


# def search_species(ui, query):
#     print(query)
#     ui.results = blah
# function for each button, which does a query and updates ui


app = cervoui.QtWidgets.QApplication(sys.argv)
MainWindow = cervoui.QtWidgets.QMainWindow()
ui = cervoui.Ui_MainWindow()
ui.setupUi(MainWindow)
# search_callback = lambda: search_species(ui, ui.searchBar.value)
# ui.searchButton.
MainWindow.show()
sys.exit(app.exec_())
