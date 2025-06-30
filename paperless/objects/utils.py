import attr

NO_UPDATE = object()


def convert_cls(cl):
    """If the attribute is an instance of cls and not None, pass, else try constructing."""

    def converter(val):
        if val is None:
            return None
        elif isinstance(val, cl):
            return val
        else:
            return safe_init(cl, val)

    return converter


def convert_iterable(cl):
    def converter(iterable):
        result = []
        for val in iterable:
            if isinstance(val, cl):
                result.append(val)
            else:
                result.append(safe_init(cl, val))
        return result

    return converter


def optional_convert(convert):
    """Invoke the subconverter only if the value is present."""

    def optional_converter(val):
        if val is None:
            return None
        elif val is NO_UPDATE:
            return NO_UPDATE
        else:
            return convert(val)

    return optional_converter


def convert_dictionary(cl):
    def converter(d):
        result = dict()
        for key, val in d.items():
            if isinstance(val, cl):
                result[key] = val
            else:
                result[key] = safe_init(cl, val)
        return result

    return converter


def tax_rate_validator(instance, attribute, value):
    if value == NO_UPDATE:
        return

    if isinstance(value, str):
        value = float(value)
    if value < 0:
        raise ValueError(
            "Invalid tax rate. Rate cannot be below 0%. {} provided.".format(value)
        )
    elif value > 100:
        raise ValueError(
            "Invalid tax rate. Rate cannot be above 100%. {} provided.".format(value)
        )


def positive_number_validator(instance, attribute, value):
    return value >= 0


def numeric_validator(instance, attribute, value):
    return isinstance(value, int) or isinstance(value, float)


def safe_init(attrs_class, value_dict):
    """Safely instantiate an attrs class instance with protection against extra
    kwargs. This ensures forward compatibility with fields added in the API."""
    if not attr.has(attrs_class):
        return attrs_class(**value_dict)
    safe_dict = {
        attr.name: value_dict.get(attr.name) for attr in attr.fields(attrs_class)
    }
    return attrs_class(**safe_dict)


def get_metadata_filter_query_params(metadata: dict):
    params = {}
    for k, v in metadata.items():
        key = f'metadata[{k}]'
        params[key] = v
    return params
