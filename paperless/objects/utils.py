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
        return [cl(**val) for val in iterable]
    return converter

def phone_length_validator(instance, attribute, value):
    if len(str(value)) is not 10:
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