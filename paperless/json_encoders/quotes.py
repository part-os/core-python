from paperless.json_encoders import SmartJSONEncoder


class QuoteEncoder(SmartJSONEncoder):
    basic_field_keys = ['erp_code']
