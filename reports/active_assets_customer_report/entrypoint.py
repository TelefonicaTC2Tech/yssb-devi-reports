# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Telefónica Cybersecurity & Cloud Tech
#

from connect.client import R

from reports.fields import Field, Fields
from reports.utils import  convert_to_datetime, get_value, get_value_from_array_by_id 

DATA_GEOGRAPHY = "DE"
BILLING_TYPE = "usage"
FAX = ""
ADDRESS_1 = "Ronda de la comunicación S/N"
NOT_APPLY = "N/A"
MADRID = "Madrid"
COUNTRY_CODE = "ES"
POSTAL_CODE = "28050"

FIELDS = Fields((
    Field('creation date', lambda r: convert_to_datetime(get_value(r, 'events.created.at'))),
    Field('Asset id', lambda r: get_value(r, 'id')),
    Field('Name', lambda r: get_value(r, 'tiers.customer.tax_id')),
    Field('Show as', lambda r: get_value(r, 'tiers.customer.name')),
    Field('Data Geography', lambda r: DATA_GEOGRAPHY),
    Field('Billing Type', lambda r: BILLING_TYPE), 
    Field('First name', lambda r: get_firstname_from_fullname(get_value_from_array_by_id(r, 'params', 'technicalContact', 'value'))),
    Field('Last name', lambda r: get_lastname_from_fullname(get_value_from_array_by_id(r, 'params', 'technicalContact', 'value'))),
    Field('Technical Email', lambda r: get_value_from_array_by_id(r, 'params', 'technicalEmail', 'value')),
    Field('Phone', lambda r: get_value_from_array_by_id(r, 'params', 'sede', 'value')),
    Field('Mobile', lambda r: get_value_from_array_by_id(r, 'params', 'technicalPhone', 'value')),
    Field('Fax', lambda r: FAX),
    Field('Address 1', lambda r: ADDRESS_1),
    Field('Address 2', lambda r: NOT_APPLY),
    Field('Address 3', lambda r: NOT_APPLY),
    Field('City', lambda r: MADRID),
    Field('State', lambda r: MADRID),
    Field('Country Code', lambda r: COUNTRY_CODE),
    Field('State', lambda r: POSTAL_CODE),
))

def get_firstname_from_fullname(fullname):
    strtoken = fullname.strip().split(' ')
    if len(strtoken) > 0:
        return strtoken[0]
    else:
        return ""
    
def get_lastname_from_fullname(fullname):
    strtoken = fullname.strip().split(' ')
    if len(strtoken) > 0:
        strtoken.pop(0) # Remove first name
        return ' '.join(strtoken)
    else:
        return ""

def generate(
    client=None,
    parameters=None,
    progress_callback=None,
    renderer_type=None,
    extra_context_callback=None,
):
    assets = _get_assets(client, parameters)  
    progress = 0
    total = assets.count()
    if renderer_type == 'csv':
        yield FIELDS.names()
        progress += 1
        total += 1
        progress_callback(progress, total)

    for asset in assets:
        values = FIELDS.process(asset)
        if renderer_type == 'json':
            yield dict(zip(FIELDS.json_names(), values))
        else:
            yield values
        progress += 1
        progress_callback(progress, total)

def _get_assets(client, parameters):
    query = R()
    if parameters.get('mkp') and parameters['mkp']['all'] is False:
        query &= R().marketplace.id.oneof(parameters['mkp']['choices'])  
    if parameters.get('rr_status') and parameters['rr_status']['all'] is False:
        query &= R().status.oneof(parameters['rr_status']['choices'])
    if parameters.get('environment') and parameters['environment']['all'] is False:
        query &= R().connection.type.oneof(parameters['environment']['choices'])
    
    return client('subscriptions').assets.filter(query)
