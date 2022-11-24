# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Telefónica Cybersecurity & Cloud Tech
#

from connect.client import R

from reports.fields import Field, Fields
from reports.utils import convert_to_datetime, convert_to_int, get_value, get_value_from_array_by_id, get_value_from_array_by_key

NEXTGENERATION_EU_SUBSIDIZED_MPN = 'SEC_SMB_REC_FUNDS'

FIELDS = Fields((
    Field('Request ID', lambda r: get_value(r, 'id')),
    Field('Updated At', lambda r: convert_to_datetime(get_value(r, 'updated'))),
    Field('Customer ID', lambda r: get_value(r, 'asset.tiers.customer.id')),
    Field('Customer Name', lambda r: get_value(r, 'asset.tiers.customer.name')),
    Field('Customer TaxID', lambda r: get_value(r, 'asset.tiers.customer.tax_id')),    
    Field('EU Fund New Packet', lambda r: 'Basic' if _get_delta_from_item(r, NEXTGENERATION_EU_SUBSIDIZED_MPN) < 0 else 'Advanced'),
    Field('Technical Email', lambda r: get_value_from_array_by_id(r, 'asset.params', 'technicalEmail', 'value')),
    Field('Technical Contact', lambda r: get_value_from_array_by_id(r, 'asset.params', 'technicalContact', 'value')),
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
        # Only process if the "NextGeneration EU subsidized" item quantity has changed
        if _get_delta_from_item(request, NEXTGENERATION_EU_SUBSIDIZED_MPN) != 0:
            values = FIELDS.process(request)
            if renderer_type == 'json':
                yield dict(zip(FIELDS.json_names(), values))
            else:
                yield values
        progress += 1
        progress_callback(progress, total)


def _get_requests(client, parameters):
    all_connections = ['production']
    all_types = ['change']
    all_status = ['approved']

    query = R()
    query &= R().updated.ge(parameters['date']['after'])
    query &= R().updated.le(parameters['date']['before'])

    if parameters.get('product') and parameters['product']['all'] is False:
        query &= R().asset.product.id.oneof(parameters['product']['choices'])
    if parameters.get('rr_type') and parameters['rr_type']['all'] is False:
        query &= R().type.oneof(parameters['rr_type']['choices'])
    else:
        query &= R().type.oneof(all_types)
    if parameters.get('rr_status') and parameters['rr_status']['all'] is False:
        query &= R().status.oneof(parameters['rr_status']['choices'])
    else:
        query &= R().status.oneof(all_status)
    if parameters.get('mkp') and parameters['mkp']['all'] is False:
        query &= R().asset.marketplace.id.oneof(parameters['mkp']['choices'])
    if parameters.get('hub') and parameters['hub']['all'] is False:
        query &= R().asset.connection.hub.id.oneof(parameters['hub']['choices'])
    else:
        query &= R().asset.connection.type.oneof(all_connections)
    if parameters.get('environment') and parameters['environment']['all'] is False:
        query &= R().asset.connection.type.oneof(parameters['environment']['choices'])

    return client.requests.filter(query)

def _get_delta_from_item(request, item_mpn):
    old_quantity = int(get_value_from_array_by_key(request, 'asset.items', 'mpn', item_mpn, 'old_quantity', '0'))
    quantity = int(get_value_from_array_by_key(request, 'asset.items', 'mpn', item_mpn, 'quantity', '0'))
    return quantity - old_quantity