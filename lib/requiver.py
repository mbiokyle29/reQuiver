"""
Requiver
author: Kyle McChesney

Main class file, for Requiver. For interacting with Archer DX Quiver database

"""
import requests
#from bs4 import BeautifulSoup

class Requiver(object):

    def __init__(self):
        self._raw_endpoint = "http://quiver.archerdx.com/results?query="
        self._sesh = requests.Session()

    def query(self, query):
        query_str = self._raw_endpoint + query
        res = self._sesh.get(query_str)
        return res

class GeneFushion(object):

    def __init__(self, l_gene, r_gene, evidence):
        self.name = "{}:{}".format(l_gene.rstrip(), r_gene.rstrip())
        self.l_gene = l_gene
        self.r_gene = r_gene
        self.evidence = evidence