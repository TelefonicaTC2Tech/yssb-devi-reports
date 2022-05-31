# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Telefónica Cybersecurity & Cloud Tech
#

from connect.client import R

from reports.fields import Field, Fields
from reports.utils import convert_to_datetime, get_value, today_str

FIELDS = Fields((
    Field('Request ID', lambda r, _: get_value(r, 'id')),
    Field('Request Type', lambda r, _: get_value(r, 'type')),
    Field('Request Status', lambda r, _: get_value(r, 'status')),
    Field('Created At', lambda r, _: convert_to_datetime(get_value(r, 'created'))),
    Field('Updated At', lambda r, _: convert_to_datetime(get_value(r, 'updated'))),
    Field('Exported At', lambda _, __: today_str()),
    Field('Customer ID', lambda r, _: get_value(r, 'asset.tiers.customer.id')),
    Field('Customer Name', lambda r, _: get_value(r, 'asset.tiers.customer.name')),
    Field('Customer TaxID', lambda r, _: get_value(r, 'asset.tiers.customer.tax_id')),
    Field('Customer External ID', lambda r, _: get_value(r, 'asset.tiers.customer.external_id')),
    Field('Tier 1 ID', lambda r, _: get_value(r, 'asset.tiers.tier1.id')),
    Field('Tier 1 Name', lambda r, _: get_value(r, 'asset.tiers.tier1.name')),
    Field('Tier 1 External ID', lambda r, _: get_value(r, 'asset.tiers.tier1.external_id')),
    Field('Tier 2 ID', lambda r, _: get_value(r, 'asset.tiers.tier2.id')),
    Field('Tier 2 Name', lambda r, _: get_value(r, 'asset.tiers.tier2.name')),
    Field('Tier 2 External ID', lambda r, _: get_value(r, 'asset.tiers.tier2.external_id')),
    Field('Provider  ID', lambda r, _: get_value(r, 'asset.connection.provider.id')),
    Field('Provider Name', lambda r, _: get_value(r, 'asset.connection.provider.name')),
    Field('Vendor ID', lambda r, _: get_value(r, 'asset.connection.vendor.id')),
    Field('Vendor Name', lambda r, _: get_value(r, 'asset.connection.vendor.name')),
    Field('Product ID', lambda r, _: get_value(r, 'asset.product.id')),
    Field('Product Name', lambda r, _: get_value(r, 'asset.product.name')),
    Field('Asset ID', lambda r, _: get_value(r, 'asset.id')),
    Field('Asset External ID', lambda r, _: get_value(r, 'asset.external_id')),
    Field('Transaction Type', lambda r, _: get_value(r, 'asset.connection.type')),
    Field('Hub ID', lambda _, c: get_value(c, 'hub.id')),
    Field('Hub Name', lambda _, c: get_value(c, 'hub.name')),
    Field('Asset Status', lambda r, _: get_value(r, 'asset.status')),
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
        values = FIELDS.process(request)
        if renderer_type == 'json':
            yield dict(zip(FIELDS.json_names(), values))
        else:
            yield values
        progress += 1
        progress_callback(progress, total)


def _get_requests(client, parameters):
    all_types = ['tiers_setup', 'inquiring', 'pending', 'approved', 'failed', 'draft']

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

    return client.requests.filter(query)
