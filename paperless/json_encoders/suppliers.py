from paperless.json_encoders import SmartJSONEncoder
from paperless.json_encoders.customers import AddressEncoder


class SupplierFacilityEncoder(SmartJSONEncoder):
    basic_field_keys = ['name', 'is_default', 'phone', 'phone_ext', 'url']

    sub_encoders = [('address', AddressEncoder)]
