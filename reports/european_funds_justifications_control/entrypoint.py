# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Telefónica Cybersecurity & Cloud Tech
#

from connect.client import R

from reports.fields import Field, Fields
from reports.utils import convert_to_datetime, convert_to_int, get_value, get_value_from_array_by_id, get_value_from_array_by_key

# Items of the basic packet for EU funds
ITEMS_BASIC = [
    'Antivirus Antiransomware',
    'Secure Browsing',
    'Clean email',
    'Awareness',
]
# Items that cannot be present in the basic packet for EU funds
ITEMS_NOT_BASIC = [
    'Secure Remote Access',
    'Secure Office',
    'NextGeneration EU subsidized',
    'Protected Cloud  Services' # There is a typo in this item name with extra space!
]
# Items in the advanced packet for EU funds
ITEMS_ADVANCED = ITEMS_BASIC + [
    'Secure Remote Access',
    'Secure Office',
    'NextGeneration EU subsidized'
]


FIELDS = Fields((
    Field('Request ID', lambda r: get_value(r, 'id')),
    Field('Subscription Type', lambda r: get_value(r, 'type')),
    Field('Created At', lambda r: convert_to_datetime(get_value(r, 'created'))),
    Field('Customer ID', lambda r: get_value(r, 'asset.tiers.customer.id')),
    Field('Technical Email', lambda r: get_value_from_array_by_id(r, 'asset.params', 'technicalEmail', 'value')),
    Field('Last Change At', lambda r: convert_to_datetime(get_value(r, 'updated'))),
    Field('Customer Name', lambda r: get_value(r, 'asset.tiers.customer.name')),
    Field('Customer TaxID', lambda r: get_value(r, 'asset.tiers.customer.tax_id')),
    Field('SubscriptionID', lambda r: get_value(r, 'asset.id')),
    Field('Antivirus Quantity', lambda r: convert_to_int(get_value_from_array_by_key(r, 'asset.items', 'display_name', 'Antivirus Antiransomware', 'quantity'))),
    Field('EU Fund Packet', lambda r: _get_european_fund_packet(r)),
    Field('Technical Contact', lambda r: get_value_from_array_by_id(r, 'asset.params', 'technicalContact', 'value')),
    Field('Postal Address', lambda r: get_value_from_array_by_id(r, 'asset.params', 'postalAddress', 'value')),
    Field('Domain', lambda r: get_value_from_array_by_id(r, 'asset.params', 'domain', 'value')),
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
    all_connections = ['production']

    query = R()
    query &= R().created.ge(parameters['date']['after'])
    query &= R().created.le(parameters['date']['before'])

    if parameters.get('product') and parameters['product']['all'] is False:
        query &= R().asset.product.id.oneof(parameters['product']['choices'])
    if parameters.get('rr_type') and parameters['rr_type']['all'] is False:
        query &= R().type.oneof(parameters['rr_type']['choices'])
    if parameters.get('rr_status') and parameters['rr_status']['all'] is False:
        query &= R().status.oneof(parameters['rr_status']['choices'])
    if parameters.get('mkp') and parameters['mkp']['all'] is False:
        query &= R().asset.marketplace.id.oneof(parameters['mkp']['choices'])
    if parameters.get('environment') and parameters['environment']['all'] is False:
        query &= R().asset.connection.type.oneof(parameters['environment']['choices'])

    return client.requests.filter(query)


def _exists_item(request, item_name):
    return get_value_from_array_by_key(request, 'asset.items', 'display_name', item_name, 'quantity', '0') != '0'


def _get_european_fund_packet(request):
    if all(map(lambda x: _exists_item(request, x), ITEMS_ADVANCED)):
        return 'Advanced'
    if all(map(lambda x: _exists_item(request, x), ITEMS_BASIC)) and not any(map(lambda x: _exists_item(request, x), ITEMS_NOT_BASIC)):
        return 'Basic'
    return ''
