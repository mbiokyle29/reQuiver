"""
exceptions.py
author: Kyle McChesney

Exceptions for reQuiver

"""

class EmptyQueryStringException(Exception):

    def __str__(self):
        return "Query parameter to .query cannot be empty"

class NetworkErrorException(Exception):

    def __init__(self, code):
        self.code = code

    def __str__(self):
        return "Network Error: Request returned error code: {}".format(self.code)