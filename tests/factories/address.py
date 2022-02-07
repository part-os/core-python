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
