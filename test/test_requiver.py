#!/usr/bin/env python
"""
test_requvier.py
author: Kyle McChesney
"""

import unittest
import lib
import os
import logging
log = logging.getLogger(__name__)

class RequiverTest(unittest.TestCase):

    def testRequiverCreation(self):

        rq = lib.Requiver()
        end_point = "http://quiver.archerdx.com/results?query="

        self.assertEqual(type(rq), lib.Requiver)
        self.assertEqual(rq._raw_endpoint, end_point)

    def testRequiverQuerySingleGene(self):

        rq = lib.Requiver()
        query_gene = "NOTCH1" # some example