# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Telefónica Cybersecurity & Cloud Tech
#

from datetime import datetime
from threading import Lock


def convert_to_datetime(param_value):
    if param_value == "" or param_value == "-":
        return "-"

    return datetime.strptime(
        param_value.replace("T", " ").replace("+00:00", ""),
        "%Y-%m-%d %H:%M:%S",
    )

def convert_to_int(param_value):
    try:
        return int(param_value)
    except:
        ''

def today_str():
    return datetime.today().strftime('%Y-%m-%d %H:%M:%S')

def get_value(d, path, default='-'):
    """
    Return the value of a nested dictionary where 'path' targets
    the value in the nested dictionary.
    The path contains multiple keys joined by '.' character.
    """
    if not d:
        return default
    keys = path.split('.')
    v = d
    for key in keys:
        if key not in v:
            return default
        v = v[key]
    return v

def get_value_from_array_by_id(d, array_path, id, path, default='-'):
    """
    Return the value of a nested dictionary where array_path targets an
    array of dictionaries, and it looks for an item with a specific 'id'.
    Finally, the value is retrieved from the 'path' inside that item.
    """
    return get_value_from_array_by_key(d, array_path, 'id', id, path, default)

def get_value_from_array_by_key(d, array_path, key, value, path, default='-'):
    """
    Return the value of a nested dictionary where array_path targets an
    array of dictionaries, and it looks for an item with a specific key value.
    Finally, the value is retrieved from the 'path' inside that item.
    """
    items = get_value(d, array_path, default)
    if type(items) is not list:
        return default
    for item in items:
        if item.get(key) == value:
            return get_value(item, path, default)
    return default


class Progress:
    def __init__(self, callback, total):
        self.lock = Lock()
        self.current = 0
        self.total = total
        self.callback = callback

    def increment(self):
        self.lock.acquire()
        self.current += 1
        self.callback(self.current, self.total)
        self.lock.release()
