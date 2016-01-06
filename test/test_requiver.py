#!/usr/bin/env python
"""
test_requvier.py
author: Kyle McChesney
"""

import unittest
from requiver import Requiver, QuiverFushionPlexPanel, QuiverGeneFushion
from requiver.exceptions import EmptyQueryStringException, NetworkErrorException
from httmock import urlmatch, HTTMock, response
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

    @urlmatch(netloc=r'(.*\.)?quiver\.archerdx\.com', path="/results", query="query=404MEPLEASE")
    def mock_network_error(self, url, request):
        return response(404, "ERROR", {}, {}, 5, request)

    def setUp(self):        
        self.req = Requiver()

    def test_no_res(self):
        
        with HTTMock(self.mock_no_res_page):
            no_results_get = self.req.query("ZZZZZ")
            self.assertEqual(len(no_results_get.panels), 0)
            self.assertEqual(len(no_results_get.fusions), 0)

    def test_single_gene_res(self):
        
        with HTTMock(self.mock_single_gene_page):
            notch_get = self.req.query("NOTCH1")
            self.assertNotEqual(len(notch_get.panels), 0)
            self.assertNotEqual(len(notch_get.fusions), 0)

            for panel in notch_get.panels:
                self.assertEqual(type(panel), QuiverFushionPlexPanel)

            for fusion in notch_get.fusions:
                self.assertEqual(type(fusion), QuiverGeneFushion)

    def test_query_set_in_results(self):

        with HTTMock(self.mock_single_gene_page):
            notch_get = self.req.query("NOTCH1")
            self.assertEqual(notch_get.query_term, "NOTCH1")

    def test_empty_string_exception(self):

        # dont need a mock no request will fire
        self.assertRaises(EmptyQueryStringException, self.req.query, "")

    def test_network_exception(self):

        with HTTMock(self.mock_network_error):
            self.assertRaises(NetworkErrorException, self.req.query, "404MEPLEASE")