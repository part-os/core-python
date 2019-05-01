import factory
from faker import Faker

from paperless.objects.address import Address
from .fuzzies import FuzzyPhoneExt, FuzzyPhoneNumber

fake = Faker()

class AddressFactory(factory.Factory):
    class Meta:
        model = Address
        strategy = factory.BUILD_STRATEGY

    address1 = fake.street_address()
    address2 = fake.secondary_address()
    business_name = fake.company()
    city = fake.city()
    country = factory.fuzzy.FuzzyChoice(choices=['USA', 'CA'])
    first_name = fake.first_name()
    last_name = fake.last_name()
    phone = FuzzyPhoneNumber()
    phone_ext = FuzzyPhoneExt()
    postal_code = fake.postalcode_plus4()
    state = fake.state()



"""
address1: str = attr.ib(validator=attr.validators.instance_of(str))
city: str = attr.ib(validator=attr.validators.instance_of(str))
country: str = attr.ib(validator=attr.validators.in_(['CA', 'USA']))
postal_code: str = attr.ib(validator=attr.validators.instance_of(str))
state: str = attr.ib(
    validator=attr.validators.instance_of(str))  # TODO: DO I WANT THIS TO BE A SATE OR SHOULD THIS BE INTERNATIONAL?

# optional fields
address2: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
business_name: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)),
                                       default=None)
first_name: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
last_name: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
phone: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
phone_ext: Optional[str] = attr.ib(validator=attr.validators.optional(attr.validators.instance_of(str)), default=None)
"""