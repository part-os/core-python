from paperless.json_encoders import SmartJSONEncoder


class OrderEncoder(SmartJSONEncoder):
    basic_field_keys = [
        'erp_code'
    ]
