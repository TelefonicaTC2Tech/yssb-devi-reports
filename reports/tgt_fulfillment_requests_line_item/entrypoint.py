# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, CloudBlue
# All rights reserved.
#

from connect.client import R

from reports.fields import Field, Fields
from reports.utils import convert_to_datetime, get_value


FIELDS = Fields((
    Field('Request_ID', lambda r: get_value(r['request'], 'id')),
    Field('Request_Type', lambda r: get_value(r['request'], 'type')),
    Field('Request_Status', lambda r: get_value(r['request'], 'status')),
    Field('Created_At', lambda r: convert_to_datetime(get_value(r['request'], 'created'))),
    Field('Updated_At', lambda r: convert_to_datetime(get_value(r['request'], 'updated'))),
    Field('Item_Name', lambda r: get_value(r['item'], 'display_name')),
    Field('Item_MPN', lambda r: get_value(r['item'], 'mpn')),
    Field('Quantity', lambda r: get_value(r['item'], 'quantity')),
    Field('Customer_ID', lambda r: get_value(r['request'], 'asset.tiers.customer.id')),
    Field('Customer_External_ID', lambda r: get_value(r['request'], 'asset.tiers.customer.external_id')),
    Field('Customer_Name', lambda r: get_value(r['request'], 'asset.tiers.customer.name')),
    Field('Asset_ID', lambda r: get_value(r['request'], 'asset.id')),
    Field('Asset_External_ID', lambda r: get_value(r['request'], 'asset.external_id')),
    Field('Asset_Status', lambda r: get_value(r['request'], 'asset.status').capitalize() if get_value(r['request'], 'asset.status') != '-' else '-'),
))


def generate(
    client=None,
    parameters=None,
    progress_callback=None,
    renderer_type=None,
    extra_context_callback=None,
):
    requests = _get_requests(client, parameters)
    total = requests.count()
    progress = 0
    if renderer_type == 'csv':
        yield FIELDS.names()
        total += 1
        progress += 1
        progress_callback(progress, total)

    for request in requests:
        for item in request['asset']['items']:
            if item['quantity'] != 0 and item['old_quantity'] != 0:
                values = FIELDS.process({'request': request, 'item': item})
                if renderer_type == 'json':
                    yield dict(zip(FIELDS.json_names(), values))
                else:
                    yield list(values)
        progress += 1
        progress_callback(progress, total)


def _get_requests(client, parameters):
    all_types = ['tiers_setup', 'inquiring', 'pending', 'approved', 'failed']

    query = R()
    query &= R().created.ge(parameters['date']['after'])
    query &= R().created.le(parameters['date']['before'])

    if parameters.get('product') and parameters['product']['all'] is False:
        query &= R().asset.product.id.oneof(parameters['product']['choices'])
    if parameters.get('rr_type') and parameters['rr_type']['all'] is False:
        query &= R().type.oneof(parameters['rr_type']['choices'])
    if parameters.get('rr_status') and parameters['rr_status']['all'] is False:
        query &= R().status.oneof(parameters['rr_status']['choices'])
    else:
        query &= R().status.oneof(all_types)
    if parameters.get('mkp') and parameters['mkp']['all'] is False:
        query &= R().asset.marketplace.id.oneof(parameters['mkp']['choices'])
    if parameters.get('hub') and parameters['hub']['all'] is False:
        query &= R().asset.connection.hub.id.oneof(parameters['hub']['choices'])

    return client.requests.filter(query).select(
        '-asset.params,'
        '-asset.configuration',
        '-activation_key',
        '-template',
    )
