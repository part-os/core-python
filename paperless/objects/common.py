import decimal
from decimal import Decimal, DecimalException
from typing import Optional
import math
import attr

from .utils import positive_number_validator

ROUND_TO = Decimal('0.01')
DECIMAL_PLACES = 2


@attr.s(frozen=True, cmp=False)
class Money:
    """Represents a USD currency value, encapsulates rounding logic and conversion to cents."""

    raw_amount: Decimal = attr.ib(
        converter=Decimal, validator=positive_number_validator, default=Decimal(0)
    )
    currency: str = 'USD'

    @property
    def dollars(self):
        try:
            return self.rounded()
        except DecimalException:
            return 'NaN'

    def rounded(
            self, precision: int = DECIMAL_PLACES, rounding=decimal.ROUND_HALF_EVEN
    ) -> Decimal:
        """
        Round the Money to a specified amount of decimal places.
        Defaults to 2.
        """
        precision = precision or DECIMAL_PLACES
        return self.raw_amount.quantize(
            Decimal(str(math.pow(10, -precision))), rounding=rounding
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


@attr.s(frozen=False)
class Salesperson:
    email: str = attr.ib(validator=attr.validators.instance_of(str))
    first_name: Optional[str] = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )
    last_name: Optional[str] = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )
    erp_code: Optional[str] = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )
