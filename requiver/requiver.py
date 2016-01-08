"""
requiver.py
author: Kyle McChesney

Main class file, for reQuiver. 
"""
import requests
from bs4 import BeautifulSoup
from cachecontrol import CacheControl

from utils import panel_table_filter, fusion_table_filter, clean_string
from exceptions import EmptyQueryStringException, NetworkErrorException


class reQuiver(object):

    def __init__(self):
        self._raw_endpoint = "http://quiver.archerdx.com/results?query="
        self._sesh = CacheControl(requests.Session())

    def query(self, query):

        if len(query) == 0:
            raise EmptyQueryStringException()

        q_string = self._raw_endpoint + str(query)
        response = self._sesh.get(q_string)

        if response.status_code != 200:
            raise NetworkErrorException(response.status_code)

        soup = BeautifulSoup(response.content, "html.parser")

        # parse the panels
        panels = soup.find(panel_table_filter)
        panels_list  = []
        
        if panels is not None:
            for row in panels.find_all("tr"):
                cells = row.find_all("td")
                
                if len(cells) == 2:
                    link = cells[0].a['href']
                    genes = [clean_string(gene) for gene in cells[1].string.split()]
                    panels_list.append(QuiverFushionPlexPanel(link, genes))

        # parse the fusions
        fusions = soup.find_all(fusion_table_filter)
        fusions_list = []

        if fusions is not None:
            for fusion in fusions:
                table = fusion.find('table')
                for row in table.find_all('tr'):
                    cells = row.find_all('td')
                    if len(cells) != 2:

                        # get the link
                        link = cells[0].a['href']
                        original_annotation = clean_string(cells[1].string)
                        disease = cells[2].string.strip()
                        pubmed_link = cells[3].a['href']
                        evidence_count = int(cells[4].string)

                        fusions_list.append(QuiverGeneFushion(link, original_annotation, disease,
                                            pubmed_link, evidence_count))

        return QuiverResultSet(panels_list, fusions_list, query)

class QuiverFushionPlexPanel(object):

    def __init__(self, link, genes):
        self.link = link
        self.genes = genes

    def __str__(self):
        return "<FusionPlexPanel: [{}] {} >".format(", ".join(self.genes), self.link)

class QuiverGeneFushion(object):

    def __init__(self, link, annotation, disease, pubmed_link, evidence_count):
        self.link = link
        self.annotation = annotation
        self.disease = disease
        self.pubmed_link = pubmed_link
        self.evidence_count = evidence_count

    def __str__(self):
        return "<GeneFusion: {}>".format(self.annotation)

class QuiverResultSet(object):

    def __init__(self, panels, fusions, query):
        self.panels = panels
        self.fusions = fusions
        self.query_term = query

    def summary(self):
        summary = "Quiver Results Summary: \n\n"
        
        summary += "Found {} panels\n".format(str(len(self.panels)))
        summary += "\n".join([str(panel) for panel in self.panels])
        
        summary += "\n\nFound {} fusions\n".format(str(len(self.fusions)))
        summary += "\n".join([str(fusion) for fusion in self.fusions])

        print summary
