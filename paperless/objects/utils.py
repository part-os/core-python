NO_UPDATE = object()


def convert_cls(cl):
    """If the attribute is an instance of cls and not None, pass, else try constructing."""

    def converter(val):
        if val is None:
            return None
        elif isinstance(val, cl):
            return val
        else:
            return cl(**val)

    return converter


def convert_iterable(cl):
    def converter(iterable):
        result = []
        for val in iterable:
            if isinstance(val, cl):
                result.append(val)
            else:
                result.append(cl(**val))
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
                result[key] = cl(**val)
        return result

    return converter


def phone_length_validator(instance, attribute, value):
    if len(value) != 10:
        raise ValueError(
            "Invalid phone number for {}. Phone number must be 10 digits.".format(
                attribute
            )
        )


def tax_rate_validator(instance, attribute, value):
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
