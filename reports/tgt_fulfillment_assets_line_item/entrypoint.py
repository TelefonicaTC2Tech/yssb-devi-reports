# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, CloudBlue
# All rights reserved.
#

from connect.client import R

from reports.fields import Field, Fields
from reports.utils import convert_to_datetime, get_value, get_value_from_array_by_id, get_value_from_array_by_key


FIELDS = Fields((
    Field('Asset_ID', lambda x: get_value(x['asset'], 'id')),
    Field('Asset_External_ID', lambda x: get_value(x['asset'], 'external_id')),
    Field('Asset_Status', lambda x: get_value(x['asset'], 'status').capitalize() if get_value(x['asset'], 'status') != '-' else '-'),
    Field('Created_At', lambda x: convert_to_datetime(get_value(x['asset'], 'events.created.at'))),
    Field('Updated_At', lambda x: convert_to_datetime(get_value(x['asset'], 'events.updated.at'))),
    Field('Item_Name', lambda x: get_value(x['item'], 'display_name')),
    Field('Item_MPN', lambda x: get_value(x['item'], 'mpn')),
    Field('Quantity', lambda x: get_value(x['item'], 'quantity')),
    Field('Customer_ID', lambda x: get_value(x['asset'], 'tiers.customer.id')),
    Field('Customer_External_ID', lambda x: get_value(x['asset'], 'tiers.customer.external_id')),
    Field('Customer_Name', lambda x: get_value(x['asset'], 'tiers.customer.name')),
    Field('Marketplace', lambda x: get_value(x['asset'], 'marketplace.id')),
    Field('domain', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name' ,'domain', 'value')),
    Field('postalAddress', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'postalAddress', 'value')),
    Field('salesTEemail', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'salesTEemail', 'value')),
    Field('sede', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'sede', 'value')),
    Field('technicalContact', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'technicalContact', 'value')),
    Field('technicalEmail', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'technicalEmail', 'value')),
    Field('technicalPhone', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'technicalPhone', 'value')),
    Field('Antivirus_Provider', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'Antivirus_Provider', 'value')),
    Field('xdr_av_installation', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'xdr_av_installation', 'value')),
    Field('AntivirusWindowsSophos', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'AntivirusWindowsSophos', 'value')),
    Field('AntivirusLinuxSophos', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'AntivirusLinuxSophos', 'value')),
    Field('AntivirusMACSophos', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'AntivirusMACSophos', 'value')),
    Field('MobileConnectionCodeSophos', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'MobileConnectionCode', 'value')),
    Field('Sophos_Tenant_id', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'Sophos_Tenant_id', 'value')),
    Field('CrowdStrike_CID', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'CrowdStrike_CID', 'value')),
    Field('CrowdStrike_Customer-ID_with_Checksum_CCID', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'CrowdStrike_Customer-ID_with_Checksum_CCID', 'value')),
    Field('CrowdStrike_Host_Group_id', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'CrowdStrike_Host_Group_id', 'value')),
    Field('CrowdStrike_Transaction_id', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'CrowdStrike_Transaction_id', 'value')),
    Field('MDR_Provisioned', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'MDR_Provisioned', 'value')),
    Field('MDR_Technical_Contact_Name', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'MDR_Technical_Contact_Name', 'value')),
    Field('MDR_Technical_Contact_Phone', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'MDR_Technical_Contact_Phone', 'value')),
    Field('MDR_technical_contact_email', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'MDR_technical_contact_email', 'value')),
    Field('Fortigate_Name', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'Fortigate_Name', 'value')),
    Field('Fortigate_Secret', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'Fortigate_Secret', 'value')),
    Field('IP_Publica', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'IP_Publica', 'value')),
    Field('id_UTM', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'id_UTM', 'value')),
    Field('utm_port', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'utm_port', 'value')),
    Field('utm_provision_status', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'utm_provision_status', 'value')),
    Field('Id_UTM_HA', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'Id_UTM_HA', 'value')),
    Field('mail_server_1', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'mail_server_1', 'value')),
    Field('mail_server_2', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'mail_server_2', 'value')),
    Field('PhishThreat', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'PhishThreat', 'value')),
    Field('secondaryTechnicalContact', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'secondaryTechnicalContact', 'value')),
    Field('secondaryTechnicalEmail', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'secondaryTechnicalEmail', 'value')),
    Field('secondaryTechnicalPhone', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'secondaryTechnicalPhone', 'value')),
    Field('Information check status', lambda x: get_value_from_array_by_key(x['asset'], 'params', 'name', 'status', 'value')),
))


def generate(
    client=None,
    parameters=None,
    progress_callback=None,
    renderer_type=None,
    extra_context_callback=None,
):
    assets = _get_assets(client, parameters)
    total = assets.count()
    progress = 0
    if renderer_type == 'csv':
        yield FIELDS.names()
        total += 1
        progress += 1
        progress_callback(progress, total)

    for asset in assets:
        for item in asset['items']:
            if item['quantity'] != 0:
                values = FIELDS.process({'asset': asset, 'item': item})
                if renderer_type == 'json':
                    yield dict(zip(FIELDS.json_names(), values))
                else:
                    yield list(values)
        progress += 1
        progress_callback(progress, total)


def _get_assets(client, parameters):
    all_connections = ['production']
    #status = ['active']

    query = R()
    #query &= x().events.created.at.ge(parameters['date']['after'])
    #query &= x().events.created.at.le(parameters['date']['before'])

    if parameters.get('mkp') and parameters['mkp']['all'] is False:
        query &= R().marketplace.id.oneof(parameters['mkp']['choices'])
    
    if parameters.get('environment') and parameters['environment']['all'] is False:
        query &= R().connection.type.oneof(parameters['environment']['choices'])
    
    if parameters.get('rr_status') and parameters['rr_status']['all'] is False:
        query &= R().status.oneof(parameters['rr_status']['choices'])


    return client('subscriptions').assets.filter(query)