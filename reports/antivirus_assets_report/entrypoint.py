# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Telefónica Cybersecurity & Cloud Tech
#

from connect.client import R

from reports.fields import Field, Fields
from reports.utils import  get_value, get_value_from_array_by_id

ANTIVIRUS_PROVIDER = "PRM-553-048-740-0050"

FIELDS = Fields((
    Field('Customer external id', lambda r: get_value(r, 'tiers.customer.external_id')),
    Field('Subscription external id', lambda r: get_value(r, 'external_id')),
    Field('Antivirus Provider', lambda r: get_value_from_array_by_id(r, 'params', ANTIVIRUS_PROVIDER, 'value', 'Trellix')),
))

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
    all_connections = ['production']
    #status = ['active']

    query = R()
    #query &= R().events.created.at.ge(parameters['date']['after'])
    #query &= R().events.created.at.le(parameters['date']['before'])

    if parameters.get('mkp') and parameters['mkp']['all'] is False:
        query &= R().marketplace.id.oneof(parameters['mkp']['choices'])

    
    if parameters.get('environment') and parameters['environment']['all'] is False:
        query &= R().connection.type.oneof(parameters['environment']['choices'])
    
    if parameters.get('rr_status') and parameters['rr_status']['all'] is False:
        query &= R().status.oneof(parameters['rr_status']['choices'])


    return client('subscriptions').assets.filter(query)
