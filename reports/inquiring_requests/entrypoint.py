# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Telefónica Cybersecurity & Cloud Tech
#

from connect.client import R

from reports.fields import Field, Fields
from reports.utils import convert_to_datetime, get_value, get_value_from_array_by_id


FIELDS = Fields((
    Field('Request ID', lambda r: get_value(r, 'id')),
    Field('Created At', lambda r: convert_to_datetime(get_value(r, 'created'))),
    Field('Last Change At', lambda r: convert_to_datetime(get_value(r, 'updated'))),
    Field('Customer ID', lambda r: get_value(r, 'asset.tiers.customer.id')),
    Field('Customer Name', lambda r: get_value(r, 'asset.tiers.customer.name')),
    Field('Customer TaxID', lambda r: get_value(r, 'asset.tiers.customer.tax_id')),
    Field('Customer External ID', lambda r: get_value(r, 'asset.tiers.customer.external_id')),
    Field('Asset ID', lambda r: get_value(r, 'asset.id')),
    Field('Asset External ID', lambda r: get_value(r, 'asset.external_id')),
    Field('TC Name Reason', lambda r: get_value_from_array_by_id(r, 'asset.params', 'technicalContact', 'value_error')),
    Field('TC e-Mail Reason', lambda r: get_value_from_array_by_id(r, 'asset.params', 'technicalEmail', 'value_error')),
    Field('TC Phone Reason', lambda r: get_value_from_array_by_id(r, 'asset.params', 'technicalPhone', 'value_error')),
    Field('Domain', lambda r: get_value_from_array_by_id(r, 'asset.params', 'domain', 'value')),
    Field('Domain Reason', lambda r: get_value_from_array_by_id(r, 'asset.params', 'domain', 'value_error')),
    Field('Sede', lambda r: get_value_from_array_by_id(r, 'asset.params', 'sede', 'value')),
    Field('Sede Reason', lambda r: get_value_from_array_by_id(r, 'asset.params', 'sede', 'value_error')),
    Field('Postal Address', lambda r: get_value_from_array_by_id(r, 'asset.params', 'postalAddress', 'value')),
    Field('Sales TE EMail', lambda r: get_value_from_array_by_id(r, 'asset.params', 'salesTEemail', 'value')),
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
    all_types = ['inquiring']
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
    else:
        query &= R().status.oneof(all_types)
    if parameters.get('mkp') and parameters['mkp']['all'] is False:
        query &= R().asset.marketplace.id.oneof(parameters['mkp']['choices'])
    if parameters.get('hub') and parameters['hub']['all'] is False:
        query &= R().asset.connection.hub.id.oneof(parameters['hub']['choices'])
    else:
        query &= R().asset.connection.type.oneof(all_connections)
    if parameters.get('environment') and parameters['environment']['all'] is False:
        query &= R().asset.connection.type.oneof(parameters['environment']['choices'])

    return client.requests.filter(query)
