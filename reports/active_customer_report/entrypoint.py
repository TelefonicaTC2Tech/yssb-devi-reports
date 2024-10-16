# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Telefónica Cybersecurity & Cloud Tech
#

from connect.client import R

from reports.fields import Field, Fields
from reports.utils import  convert_to_datetime, exists_item, get_subscription_type, get_value, get_value_from_array_by_id, get_value_from_array_by_key




FIELDS = Fields((
    Field('created_at', lambda s: convert_to_datetime(get_value(s, 'events.created.at')).strftime("%Y/%m/%d %H:%M:%S")),
    Field('customer_name', lambda s: get_value(s, 'tiers.customer.name')),
    Field('customer_external_id', lambda s: get_value(s, 'tiers.customer.external_id')),
    Field('technical_email', lambda s: get_value_from_array_by_id(s, 'params', "technicalEmail", 'value')),
    Field('technical_name', lambda s: get_value_from_array_by_id(s, 'params', "technicalContact", 'value')),
    Field('postal_address', lambda s: ''),
    Field('phone', lambda s: get_value_from_array_by_id(s, 'params', "technicalPhone", 'value')),
    Field('cif', lambda s: get_value(s, 'tiers.customer.tax_id')),
    Field('subscription_external_id', lambda s: get_value(s, 'external_id')),
    Field('sales_te_email', lambda s: get_value_from_array_by_id(s, 'params', "salesTEemail", 'value')),
    Field('domain', lambda s: get_value_from_array_by_id(s, 'params', "domain", 'value', 'SIN CORREO LIMPIO')),
    Field('subscription_name', lambda s: get_subscription_type(s, exists_item)),
    Field('ip_publica', lambda s: get_value_from_array_by_id(s, 'params', "IP_Publica", 'value')),
    Field('tier_contact_email', lambda s: get_value(s, 'tiers.customer.contact_info.contact.email')),
    Field('tier_address', lambda s: get_value(s, 'tiers.customer.contact_info.address_line1')),
    Field('tier_city', lambda s: get_value(s, 'tiers.customer.contact_info.city')),
    Field('tier_zip_code', lambda s: get_value(s, 'tiers.customer.contact_info.postal_code')),
    Field('tier_state', lambda s: get_value(s, 'tiers.customer.contact_info.city')),
    Field('tier_contact_first_name', lambda s: get_value(s, 'tiers.customer.contact_info.contact.first_name')),
    Field('tier_contact_last_name', lambda s: get_value(s, 'tiers.customer.contact_info.contact.last_name')),
    Field('tier_phone', lambda s: "{} {}".format(get_value(s, 'tiers.customer.contact_info.contact.phone_number.country_code'), get_value(s, 'tiers.customer.contact_info.contact.phone_number.phone_number'))),
    Field('digital_signature', lambda s: "Sí" if exists_item(s, "SEC_SMB_DS") else ""),
    Field('pem_premium',  lambda s: get_value_from_array_by_key(s, 'items', "mpn", "SEC_SMB_TES_ADDON_PEM", 'quantity', '')),
    Field('endpoint_active_licenses', lambda s: ''),
    Field('mobile_active_licenses', lambda s: '')
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
    
    #query &= R().status.oneof(status)

    return client('subscriptions').assets.filter(query)
