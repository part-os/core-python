import attr
import decimal
from decimal import Decimal

from .utils import positive_number_validator

ROUND_TO = Decimal('0.01')

@attr.s(frozen=True, cmp=False)
class Money:
    """Represents a USD currency value, encapsulates rounding logic and conversion to cents."""

    raw_amount: Decimal = attr.ib(
        converter=Decimal, validator=positive_number_validator, default=Decimal(0)
    )
    currency: str = 'USD'

    @property
    def dollars(self):
        return Decimal(
            self.raw_amount.quantize(ROUND_TO, rounding=decimal.ROUND_HALF_EVEN)
        )

    @property
    def cents(self) -> int:
        return int(self.dollars * 100)

    def __add__(self, other) -> 'Money':
        return attr.evolve(self, raw_amount=self.raw_amount + other.raw_amount)

    def __sub__(self, other) -> 'Money':
        return attr.evolve(self, raw_amount=self.raw_amount - other.raw_amount)

    def __le__(self, other):
        return self.dollars <= other.dollars

    def __eq__(self, other):
        return self.dollars == other.dollars

    def __bool__(self):
        return bool(self.dollars)