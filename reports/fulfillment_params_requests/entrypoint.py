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

    Field('Access_type', lambda r: get_value_from_array_by_id(r, 'asset.params', 'Access_type', 'value')),
    Field('AntivirusLinux', lambda r: get_value_from_array_by_id(r, 'asset.params', 'AntivirusLinux', 'value')),
    Field('AntivirusMAC', lambda r: get_value_from_array_by_id(r, 'asset.params', 'AntivirusMAC', 'value')),
    Field('AntivirusMoviles', lambda r: get_value_from_array_by_id(r, 'asset.params', 'AntivirusMoviles', 'value')),
    Field('AntivirusMobileApikey', lambda r: get_value_from_array_by_id(r, 'asset.params', 'AntivirusMobileApikey', 'value')),
    Field('AntivirusStandardApiKey', lambda r: get_value_from_array_by_id(r, 'asset.params', 'AntivirusStandardApiKey', 'value')),
    Field('AntivirusStandardClientId', lambda r: get_value_from_array_by_id(r, 'asset.params', 'AntivirusStandardClientId', 'value')),
    Field('AntivirusStandardClientSecret', lambda r: get_value_from_array_by_id(r, 'asset.params', 'AntivirusStandardClientSecret', 'value')),
    Field('AntivirusWindows', lambda r: get_value_from_array_by_id(r, 'asset.params', 'AntivirusWindows', 'value')),
    Field('FortiGate_Name', lambda r: get_value_from_array_by_id(r, 'asset.params', 'FortiGate_Name', 'value')),
    Field('Fortigate_Secret', lambda r: get_value_from_array_by_id(r, 'asset.params', 'Fortigate_Secret', 'value')),
    Field('IP_Publica', lambda r: get_value_from_array_by_id(r, 'asset.params', 'IP_Publica', 'value')),
    Field('Id_UTM', lambda r: get_value_from_array_by_id(r, 'asset.params', 'Id_UTM', 'value')),
    Field('Id_UTM_HA', lambda r: get_value_from_array_by_id(r, 'asset.params', 'Id_UTM_HA', 'value')),
    Field('URL_Awareness', lambda r: get_value_from_array_by_id(r, 'asset.params', 'URL_Awareness', 'value')),
    Field('awareness_registration_token', lambda r: get_value_from_array_by_id(r, 'asset.params', 'awareness_registration_token', 'value')),
    Field('domain', lambda r: get_value_from_array_by_id(r, 'asset.params', 'AntivirusLinux', 'value')),
    Field('mail_server_1', lambda r: get_value_from_array_by_id(r, 'asset.params', 'mail_server_1', 'value')),
    Field('mail_server_2', lambda r: get_value_from_array_by_id(r, 'asset.params', 'mail_server_2', 'value')),
    Field('postalAddress', lambda r: get_value_from_array_by_id(r, 'asset.params', 'postalAddress', 'value')),
    Field('salesTEemail', lambda r: get_value_from_array_by_id(r, 'asset.params', 'salesTEemail', 'value')),
    Field('sede', lambda r: get_value_from_array_by_id(r, 'asset.params', 'sede', 'value')),
    Field('status', lambda r: get_value_from_array_by_id(r, 'asset.params', 'status', 'value')),
    Field('technicalContact', lambda r: get_value_from_array_by_id(r, 'asset.params', 'technicalContact', 'value')),
    Field('technicalEmail', lambda r: get_value_from_array_by_id(r, 'asset.params', 'technicalEmail', 'value')),
    Field('technicalPhone', lambda r: get_value_from_array_by_id(r, 'asset.params', 'technicalPhone', 'value')),
    Field('utm_provision_status', lambda r: get_value_from_array_by_id(r, 'asset.params', 'utm_provision_status', 'value')),
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
    if parameters.get('environment') and parameters['environment']['all'] is False:
        query &= R().asset.connection.type.oneof(parameters['environment']['choices'])

    return client.requests.filter(query)
