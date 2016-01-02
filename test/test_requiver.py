#!/usr/bin/env python
"""
test_requvier.py
author: Kyle McChesney
"""

import unittest
from lib import Requiver
from httmock import urlmatch, HTTMock
import requests


class RequiverTest(unittest.TestCase):
    
    def gulp_html(self, file):
        res = []
        with open(file, "r+") as fh:
            for line in fh:
                res.append(line)
        return "\n".join(res)

    # MOCKS
    @urlmatch(netloc=r'(.*\.)?quiver\.archerdx\.com', path="/results", query="query=cancer")
    def mock_disease_page(self, url, request):
        return self.gulp_html('test/html/cancer.html')

    @urlmatch(netloc=r'(.*\.)?quiver\.archerdx\.com', path="/results", query="query=ZZZZZ")
    def mock_no_res_page(self, url, request):
        return self.gulp_html('test/html/no_res.html')

    @urlmatch(netloc=r'(.*\.)?quiver\.archerdx\.com', path="/results", query="query=NOTCH1")
    def mock_single_gene_page(self, url, request):
        return self.gulp_html('test/html/single_gene.html')

    def setUp(self):        
        self.req = Requiver()

    def test_no_res(self):
        
        with HTTMock(self.mock_no_res_page):
            no_results_get = self.req.query("ZZZZZ")
            self.assertTrue(False)

    def test_cancer_res(self):
        
        with HTTMock(self.mock_disease_page):
            disease_get = self.req.query("cancer")
            self.assertTrue(False)

    def test_single_gene_res(self):
        
        with HTTMock(self.mock_single_gene_page):
            disease_get = self.req.query("NOTCH1")
            self.assertTrue(False)
