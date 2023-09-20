# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Telefónica Cybersecurity & Cloud Tech
#

from connect.client import R
from enum import Enum

from reports.fields import Field, Fields
from reports.utils import  convert_to_datetime, get_request_type, get_subscription_type, get_value, get_value_from_array_by_key 

TES_SYSTEM = "TES"
PRODUCT_TIER3 = "S170_Empresa Segura"

FIELDS = Fields((
    Field('CIF', lambda r: get_value(r, 'asset.tiers.customer.tax_id')),
    Field('Customer Name', lambda r: get_value(r, 'asset.tiers.customer.name')),
    Field('Operation', lambda r: get_request_type(r)),
    Field('System', lambda r: TES_SYSTEM),
    Field('Subscription Id', lambda r: get_value(r, 'asset.id')),
    Field('Subscription', lambda r: get_subscription_type(r)),
    Field('Created At', lambda r: convert_to_datetime(get_value(r, 'asset.events.created.at'))),
    Field('Update At', lambda r: convert_to_datetime(get_value(r, 'asset.events.updated.at'))),
    Field('Product Tier3', lambda r: PRODUCT_TIER3), 
))


def generate(
    client=None,
    parameters=None,
    progress_callback=None,
    renderer_type=None,
    extra_context_callback=None,
):
    requests = _get_requests(client, parameters)
    progress = 0
    total = requests.count()
    if renderer_type == 'csv':
        yield FIELDS.names()
        progress += 1
        total += 1
        progress_callback(progress, total)

    for request in requests:
        # Only process if the subscription corresponds to european funds
        if get_request_type(request) != None:
            values = FIELDS.process(request)
            if renderer_type == 'json':
                yield dict(zip(FIELDS.json_names(), values))
            else:
                yield values
        progress += 1
        progress_callback(progress, total)


def _get_requests(client, parameters):
    all_connections = ['production']

    query = R()
    query &= R().updated.ge(parameters['date']['after'])
    query &= R().updated.le(parameters['date']['before'])

    if parameters.get('product') and parameters['product']['all'] is False:
        query &= R().asset.product.id.oneof(parameters['product']['choices'])
    if parameters.get('rr_type') and parameters['rr_type']['all'] is False:
        query &= R().type.oneof(parameters['rr_type']['choices'])
    if parameters.get('rr_status') and parameters['rr_status']['all'] is False:
        query &= R().status.oneof(parameters['rr_status']['choices'])
    if parameters.get('mkp') and parameters['mkp']['all'] is False:
        query &= R().asset.marketplace.id.oneof(parameters['mkp']['choices'])
    if parameters.get('hub') and parameters['hub']['all'] is False:
        query &= R().asset.connection.hub.id.oneof(parameters['hub']['choices'])
    else:
        query &= R().asset.connection.type.oneof(all_connections)
    if parameters.get('environment') and parameters['environment']['all'] is False:
        query &= R().asset.connection.type.oneof(parameters['environment']['choices'])

    return client.requests.filter(query)
