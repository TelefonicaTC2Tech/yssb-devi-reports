# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Telefónica Cybersecurity & Cloud Tech
#

from datetime import datetime
from connect.client import R
from enum import Enum

from reports.fields import Field, Fields
from reports.utils import  exists_asset_item, get_request_type, get_subscription_type, get_value
from soar.soar_report import send_soar_report 

TES_SYSTEM = "TES"

SOAR_ID = "67148612-3011-4905-8fb0-511feae22e9b"
SOAR_KEY = "TES"
SOAR_NAME = "Generacion automatica de informes"

FIELDS = Fields((
    Field('CIF', lambda r: get_value(r, 'asset.tiers.customer.tax_id')),
    Field('RAZON_SOCIAL', lambda r: get_value(r, 'asset.tiers.customer.name')),
    Field('EMAIL', lambda r: get_value(r, 'asset.tiers.customer.contact_info.contact.email')),
    Field('TELEFONO', lambda r: _get_phone(r)),
    Field('OPERACIÓN', lambda r: get_request_type(r)),
    Field('SISTEMA', lambda r: TES_SYSTEM),
    Field('SUBCRIPCIÓN', lambda r: get_subscription_type(r, exists_function=exists_asset_item))
))


def generate(
    client=None,
    parameters=None,
    progress_callback=None,
    renderer_type=None,
    extra_context_callback=None,
):
    start_date = datetime.now()
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
    
    end_date = datetime.now()
    if (parameters['soar_url'] != "NO_SEND" and parameters['soar_token'] != "") or \
        (parameters['soar_url'] == "CUSTOM" and parameters['soar_custom_url'] != ""):
        url = parameters['soar_custom_url'] if parameters['soar_url'] == "CUSTOM" else parameters['soar_url']
        send_soar_report(url, SOAR_ID, SOAR_KEY, SOAR_NAME, start_date, end_date, parameters['soar_token'])



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
    if parameters.get('environment') and parameters['environment']['all'] is False:
        query &= R().asset.connection.type.oneof(parameters['environment']['choices'])

    return client.requests.filter(query)

def _get_phone(request):
    country_code = get_value(request, "asset.tiers.customer.contact_info.contact.phone_number.country_code")
    area_code = get_value(request, "asset.tiers.customer.contact_info.contact.phone_number.area_code")
    phone_number = get_value(request, "asset.tiers.customer.contact_info.contact.phone_number.phone_number")
    extension = get_value(request, "asset.tiers.customer.contact_info.contact.phone_number.extension")

    return country_code + area_code + phone_number + extension
