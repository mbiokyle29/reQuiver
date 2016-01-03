"""
Requiver
author: Kyle McChesney

Main class file, for Requiver. For interacting with Archer DX Quiver database

"""
import requests
from bs4 import BeautifulSoup

class Requiver(object):

    def __init__(self):
        self._raw_endpoint = "http://quiver.archerdx.com/results?query="
        self._sesh = requests.Session()

    def panel_table_filter(self, tag):
        return tag.name == "table" and tag.th.string == "FusionPlex Panel"

    def fusion_table_filter(self, tag):
        if tag.name == "tr" and tag.has_attr('class'):
            return str(tag['class'][0]) == "results"

    def query(self, query):

        q_string = self._raw_endpoint + str(query)
        response = self._sesh.get(q_string)
        soup = BeautifulSoup(response.content, "html.parser")

        # parse the panels
        panels = soup.find(self.panel_table_filter)
        panels_list  = []
        
        if panels is not None:
            for row in panels.find_all("tr"):
                cells = row.find_all("td")
                
                if len(cells) == 2:
                    link = cells[0].a['href']
                    genes = [ self._clean_string(gene) for gene in cells[1].string.split()]
                    panels_list.append(QuiverFushionPlexPanel(link, genes))

        # parse the fusions
        fusions = soup.find_all(self.fusion_table_filter)
        fusions_list = []

        if fusions is not None:
            for fusion in fusions:
                table = fusion.find('table')
                for row in table.find_all('tr'):
                    cells = row.find_all('td')
                    if len(cells) != 2:

                        # get the link
                        link = cells[0].a['href']
                        original_annotation = self._clean_string(cells[1].string)
                        disease = cells[2].string.strip()
                        pubmed_link = cells[3].a['href']
                        evidence_count = int(cells[4].string)

                        fusions_list.append(QuiverGeneFushion(link, original_annotation, disease,
                                            pubmed_link, evidence_count))

        return QuiverResultSet(panels_list, fusions_list)

    def _clean_string(self, string):
        return str(string).replace("\s","").strip()

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

    def __init__(self, panels, fusions):
        self.panels = panels
        self.fusions = fusions