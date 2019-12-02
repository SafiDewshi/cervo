from PyQt5 import uic, QtCore, QtGui, QtWidgets
import sys
import requests

Ui_MainWindow, QtBaseClass = uic.loadUiType("cervo.ui")
localurl = "http://localhost:3030/cervo/query"


class CervoUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.searchButton.clicked.connect(self.search)

    def search(self):
        searchtext = self.searchBar.text()
        print("Searching for: " + searchtext)
        results = self.sparqlsearchspecies(searchtext)
        print(results)

    def sparqlsearchspecies(self, query):
        url = localurl
        sparql = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX cervo: <http://www.cervo.io/ontology#>
        PREFIX dbpedia2: <http://dbpedia.org/property/>


        SELECT ?name ?latinname ?zooname
        WHERE
        {{
            ?animal cervo:hasName "{}"^^xsd:string.
            ?animal cervo:hasLatinName ?latinname.
            ?animal cervo:hasName ?name.
            ?animal ^cervo:keeps-animal|cervo:is-kept-at ?zoo.
            ?zoo cervo:hasName ?zooname
        }}
        """
        sparql.format(query)
        r = requests.get(url, params={'format': 'json', 'query': query})
        results = r.json()
        return results


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CervoUI()
    window.show()
    sys.exit(app.exec_())