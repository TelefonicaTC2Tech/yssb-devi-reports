# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Telefónica Cybersecurity & Cloud Tech
#

from connect.client import R
from enum import Enum

from reports.fields import Field, Fields
from reports.utils import  get_value 

class request_type(Enum) :
    PURCHASE = "purchase"
    CANCEL = "cancel"
    CHANGE = "change"
    ADJUSTMENT = "adjustment"
    def equals(self, string):
       return self.value == string

FIELDS = Fields((
    Field('CIF', lambda r: get_value(r, 'asset.tiers.customer.tax_id')),
    Field('RAZON_SOCIAL', lambda r: get_value(r, 'asset.tiers.customer.name')),
    Field('EMAIL', lambda r: get_value(r, 'asset.tiers.customer.contact_info.contact.email')),
    Field('TELEFONO', lambda r: _get_phone(r)),
    Field('OPERACIÓN', lambda r: _get_operation(r))
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
        # Only process if the subscription corresponds to european funds
        if _get_operation(request) != None:
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
    if parameters.get('hub') and parameters['hub']['all'] is False:
        query &= R().asset.connection.hub.id.oneof(parameters['hub']['choices'])
    else:
        query &= R().asset.connection.type.oneof(all_connections)
    if parameters.get('environment') and parameters['environment']['all'] is False:
        query &= R().asset.connection.type.oneof(parameters['environment']['choices'])

    return client.requests.filter(query)

def _get_phone(request):
    country_code = get_value(request, "asset.tiers.customer.contact_info.contact.phone_number.country_code")
    area_code = get_value(request, "asset.tiers.customer.contact_info.contact.phone_number.area_code")
    phone_number = get_value(request, "asset.tiers.customer.contact_info.contact.phone_number.phone_number")
    extension = get_value(request, "asset.tiers.customer.contact_info.contact.phone_number.extension")

    return country_code + area_code + phone_number + extension

def _get_operation(request):
    type = get_value(request, "type")
    if (request_type.PURCHASE.equals(type)):
        return "A"
    elif (request_type.CANCEL.equals(type)):
        return "B"
    elif (request_type.CHANGE.equals(type) or request_type.ADJUSTMENT.equals(type)):
        return "M"
    else:
        return None