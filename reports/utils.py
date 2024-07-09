# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Telefónica Cybersecurity & Cloud Tech
#

from datetime import datetime
from enum import Enum
from threading import Lock

BASIC_SUBSCRIPTION = "Paquete Básico"
BASIC_FUNDS_SUBSCRIPTION = "Paquete Básico Fondos"
ADVANCED_SUBSCRIPTION = "Paquete Avanzado"
ADVANCED_FUNDS_SUBSCRIPTION = "Paquete Avanzado Fondos"
PREMIUM_SUBSCRIPTION = "Paquete Premium"

BASIC_PRODUCTS = ['SEC_SMB_AA', 'SEC_SMB_SB', 'SEC_SMB_CE']
BASIC_FUNDS_PRODUCTS = BASIC_PRODUCTS + ['SEC_SMB_AW']
ADVANCED_PRODUCTS = BASIC_FUNDS_PRODUCTS + ['SEC_SMB_RA', 'SEC_SMB_SO']
ADVANCED_FUNDS_PRODUCTS = ADVANCED_PRODUCTS + ['SEC_SMB_REC_FUNDS']
PREMIUM_PRODUCTS = ADVANCED_PRODUCTS + ['SEC_SMB_PCS']

class RequestType(Enum) :
    PURCHASE = "purchase"
    CANCEL = "cancel"
    CHANGE = "change"
    ADJUSTMENT = "adjustment"
    def equals(self, string):
       return self.value == string

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

def exists_asset_item(request, item_name):
    """
    Check if an item with the specified 'item_name' exists in the 'asset.items' 
    array of the given 'request' object looking by the 'mpn' value.
    
    Args:
        request (dict): The request object containing asset information.
        item_name (str): The name or identifier of the item to check.
    Returns:
        bool: True if the item exists in 'asset.items' and has a quantity greater than 0, otherwise False.
    """
    return int(get_value_from_array_by_key(request, 'asset.items', 'mpn', item_name, 'quantity', '0')) != 0

def exists_item(subscription, item_name):
    """
    Check if an item with the specified 'item_name' exists in the 'items' 
    array of the given 'subcription' object looking by the 'mpn' value.
    
    Args:
        subcription (dict): The subcription object containing items information.
        item_name (str): The name or identifier of the item to check.
    Returns:
        bool: True if the item exists in 'items' and has a quantity greater than 0, otherwise False.
    """
    return int(get_value_from_array_by_key(subscription, 'items', 'mpn', item_name, 'quantity', '0')) != 0
    
def get_subscription_type(item, exists_function):
    """
    Determine the subscription level based on the products present in the items

    This function checks the products in the 'items' properties against predefined product lists and
    returns the corresponding subscription level.

    Args:
        request (dict): The request object containing product information.

    Returns:
        str: The subscription level ('BASIC_SUBSCRIPTION', 'BASIC_FUNDS_SUBSCRIPTION',
             'ADVANCED_SUBSCRIPTION', 'ADVANCED_FUNDS_SUBSCRIPTION', 'PREMIUM_SUBSCRIPTION') if a
             matching set of products is found, otherwise an empty string.
    """
    product_to_subscription = {
        tuple(BASIC_PRODUCTS): BASIC_SUBSCRIPTION,
        tuple(BASIC_FUNDS_PRODUCTS): BASIC_FUNDS_SUBSCRIPTION,
        tuple(ADVANCED_PRODUCTS): ADVANCED_SUBSCRIPTION,
        tuple(ADVANCED_FUNDS_PRODUCTS): ADVANCED_FUNDS_SUBSCRIPTION,
        tuple(PREMIUM_PRODUCTS): PREMIUM_SUBSCRIPTION,
    }

    subscription_name = ""


    for products, label in product_to_subscription.items():
        if all(exists_function(item, x) for x in products):
            subscription_name = label

    return subscription_name

def get_request_type(request):
    """
    Determine the request type based on the 'type' field in the request.

    Args:
        request (dict): The request object containing the 'type' field.

    Returns:
        str or None: A single-character code ('A' for purchase, 'B' for cancel, 'M' for change/adjustment),
        or None if the 'type' field is not recognized.
    """
    type = get_value(request, "type")
    if (RequestType.PURCHASE.equals(type)):
        return "A"
    elif (RequestType.CANCEL.equals(type)):
        return "B"
    elif (RequestType.CHANGE.equals(type) or RequestType.ADJUSTMENT.equals(type)):
        return "M"
    else:
        return None



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
