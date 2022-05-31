# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Telefónica Cybersecurity & Cloud Tech
#

from reports.utils import get_value

class Field:
    def __init__(self, name, f):
        self._name = name
        self._f = f
    
    @property
    def name(self):
        return self._name

    @property
    def f(self):
        return self._f


class Fields:
    def __init__(self, fields):
        self._fields = fields

    def names(self):
        """Return an array with the field names"""
        return map(lambda x: x.name, self._fields)

    def json_names(self):
        """Return an array with the field names adapted to json keys."""
        return map(lambda x: x.replace(' ', '_').lower(), self.names())
    
    def process(self, request):
        """Return an array with the field values according to request parameter."""
        return map(lambda x: x.f(request), self._fields)
