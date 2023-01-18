# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, CloudBlue
# All rights reserved.
#

from connect.client import R

from reports.utils import convert_to_datetime, get_value, today_str, get_value_from_array_by_id
from reports.fields import Fields, Field

FIELDS = Fields((
    Field('Request ID', lambda r: get_value(r, 'id')),
    Field('Request Type', lambda r: get_value(r, 'type')),
    Field('Request Status', lambda r: get_value(r, 'status')),
    Field('Created At', lambda r: convert_to_datetime(get_value(r, 'created'))),
    Field('Updated At', lambda r: convert_to_datetime(get_value(r, 'updated'))),
    Field('Exported At', lambda _: today_str()),
    Field('Customer ID', lambda r: get_value(r, 'asset.tiers.customer.id')),
    Field('Customer Name', lambda r: get_value(r, 'asset.tiers.customer.name')),
    Field('Customer External ID', lambda r: get_value(r, 'asset.tiers.customer.external_id')),
    Field('Tier 1 ID', lambda r: get_value(r, 'asset.tiers.tier1.id')),
    Field('Tier 1 Name', lambda r: get_value(r, 'asset.tiers.tier1.name')),
    Field('Tier 1 External ID', lambda r: get_value(r, 'asset.tiers.tier1.external_id')),
    Field('Tier 2 ID', lambda r: get_value(r, 'asset.tiers.tier2.id')),
    Field('Tier 2 Name', lambda r: get_value(r, 'asset.tiers.tier2.name')),
    Field('Tier 2 External ID', lambda r: get_value(r, 'asset.tiers.tier2.external_id')),
    Field('Marketplace ID', lambda r: get_value(r, 'asset.marketplace.id')),
    Field('Marketplace Name', lambda r: get_value(r, 'asset.marketplace.name')),
    Field('Provider ID', lambda r: get_value(r, 'asset.connection.provider.id')),
    Field('Provider Name', lambda r: get_value(r, 'asset.connection.provider.name')),
    Field('Vendor ID', lambda r: get_value(r, 'asset.connection.vendor.id')),
    Field('Vendor Name', lambda r: get_value(r, 'asset.connection.vendor.name')),
    Field('Product ID', lambda r: get_value(r, 'asset.product.id')),
    Field('Product Name', lambda r: get_value(r, 'asset.product.name')),
    Field('Asset ID', lambda r: get_value(r, 'asset.id')),
    Field('Asset External ID', lambda r: get_value(r, 'asset.external_id')),
    Field('Transaction Type', lambda r: get_value(r, 'asset.connection.type')),
    Field('Hub ID', lambda r: get_value(r, 'asset.connection.hub.id')),
    Field('Hub Name', lambda r: get_value(r, 'asset.connection.hub.name')),
    Field('Asset Status', lambda r: get_value(r, 'asset.status')),
    Field('Email Domain', lambda r: get_value_from_array_by_id(r, 'asset.params', 'domain', 'value')),
    Field('Branch Office Address', lambda r: get_value_from_array_by_id(r, 'asset.params', 'postalAddress', 'value')),
    Field('Sales Contact Email', lambda r: get_value_from_array_by_id(r, 'asset.params', 'salesTEemail', 'value')),
    Field('Headquartes Id', lambda r: get_value_from_array_by_id(r, 'asset.params', 'sede', 'value')),
    Field('Technical Contact Name', lambda r: get_value_from_array_by_id(r, 'asset.params', 'technicalContact', 'value')),
    Field('Technical Contact Email', lambda r: get_value_from_array_by_id(r, 'asset.params', 'technicalEmail', 'value')),
    Field('Technical Contact Phone', lambda r: get_value_from_array_by_id(r, 'asset.params', 'technicalPhone', 'value')),
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
        connection = request['asset']['connection']
        values = FIELDS.process(request) 
        if renderer_type == 'json':
            yield dict(zip(FIELDS.json_names(), values))
        else:
            yield values
        progress += 1
        progress_callback(progress, total)


def _get_requests(client, parameters):
    all_status = ['tiers_setup', 'inquiring', 'pending', 'approved', 'failed']

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
        query &= R().status.oneof(all_status)
    if parameters.get('mkp') and parameters['mkp']['all'] is False:
        query &= R().asset.marketplace.id.oneof(parameters['mkp']['choices'])
    if parameters.get('hub') and parameters['hub']['all'] is False:
        query &= R().asset.connection.hub.id.oneof(parameters['hub']['choices'])

    if parameters.get('environment') and parameters['environment']['all'] is False:
        query &= R().asset.connection.type.oneof(parameters['environment']['choices'])

    return client.requests.filter(query).select(
        '-asset.items',
        '-asset.configuration',
        '-activation_key',
        '-template',
    )




# def _process_line(request, connection):
#     return (
#         get_value(request, 'id'),
#         get_value(request, 'type'),
#         get_value(request, 'status'),
#         convert_to_datetime(
#             get_value(request, 'created'),
#         ),
#         convert_to_datetime(
#             get_value(request, 'updated'),
#         ),
#         today_str(),
#         get_value(request, 'asset.tiers.customer.id'),
#         get_value(request, 'asset.tiers.customer.name'),
#         get_value(request, 'asset.tiers.customer.external_id'),
#         get_value(request, 'asset.tiers.tier1.id'),
#         get_value(request, 'asset.tiers.tier1.name'),
#         get_value(request, 'asset.tiers.tier1.external_id'),
#         get_value(request, 'asset.tiers.tier2.id'),
#         get_value(request, 'asset.tiers.tier2.name'),
#         get_value(request, 'asset.tiers.tier2.external_id'),
#         get_value(request, 'asset.marketplace.id'),
#         get_value(request, 'asset.marketplace.name'),
#         get_value(request, 'asset.connection.provider.id'),
#         get_value(request, 'asset.connection.provider.name'),
#         get_value(request, 'asset.connection.vendor.id'),
#         get_value(request, 'asset.connection.vendor.name'),
#         get_value(request, 'asset.product.id'),
#         get_value(request, 'asset.product.name'),
#         get_value(request, 'asset.id'),
#         get_value(request, 'asset.external_id'),
#         get_value(request, 'asset.connection.type'),
#         get_value(connection, 'hub.id') if 'hub' in connection else '',
#         get_value(connection, 'hub.name') if 'hub' in connection else '',
#         get_value(request, 'asset.status'),
   
#     )

