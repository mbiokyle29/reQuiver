"""
utils.py
author: Kyle McChesney

Utility functions for reQuiver
String cleaning and beautiful soup filter functions
"""

def panel_table_filter(tag):
    return tag.name == "table" and tag.th.string == "FusionPlex Panel"

def fusion_table_filter(tag):
    if tag.name == "tr" and tag.has_attr('class'):
        return str(tag['class'][0]) == "results"

def clean_string(string):
    return str(string).replace("\s","").strip()
