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
    # TODO: RAISE UNITERABLE ERROR FOR THIS
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
        return convert(val)
    return optional_converter


def phone_length_validator(instance, attribute, value):
    if len(value) is not 10:
        raise ValueError("Invalid phone number for {}. Phone number must be 10 digits.".format(
            attribute
        ))


def tax_rate_validator(instance, attribute, value):
    if value < 0:
        raise ValueError("Invalid tax rate. Rate cannot be below 0%. {} provided.".format(
            value
        ))
    elif value > 100:
        raise ValueError("Invalid tax rate. Rate cannot be above 100%. {} provided.".format(
            value
        ))
