from collections.abc import Iterable
from decimal import Decimal
from typing import TYPE_CHECKING, TypeVar

from babel.numbers import get_currency_precision, get_territory_currencies
from prices import Money, TaxedMoney, TaxedMoneyRange

if TYPE_CHECKING:
    from django.db.models import Model

PriceType = TypeVar("PriceType", TaxedMoney, Money, Decimal, TaxedMoneyRange)

# Override the get_currency_precision function
def custom_get_currency_precision(currency: str) -> int:
    if currency == 'RON':
        return 0
    return get_currency_precision(currency)

def quantize_price(price: PriceType, currency: str) -> PriceType:
    precision = custom_get_currency_precision(currency)
    number_places = Decimal(10) ** -precision
    return price.quantize(number_places)

def quantize_price_fields(model: "Model", fields: Iterable[str], currency: str) -> None:
    for field in fields:
        setattr(
            model, field, quantize_price(getattr(model, field) or Decimal(0), currency)
        )
