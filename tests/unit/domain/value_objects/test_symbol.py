import pytest

from quantforge.domain.exceptions import DomainValidationError
from quantforge.domain.value_objects import Symbol


def test_create_symbol() -> None:
    symbol = Symbol("btc", "usdt")

    assert symbol.base == "BTC"
    assert symbol.quote == "USDT"
    assert str(symbol) == "BTC/USDT"


def test_create_symbol_from_pair() -> None:
    symbol = Symbol.from_pair("eth/usdt")

    assert symbol == Symbol("ETH", "USDT")


def test_empty_base_asset() -> None:
    with pytest.raises(DomainValidationError):
        Symbol("", "USDT")


def test_empty_quote_asset() -> None:
    with pytest.raises(DomainValidationError):
        Symbol("BTC", "")


def test_same_base_and_quote_asset() -> None:
    with pytest.raises(DomainValidationError):
        Symbol("BTC", "BTC")


def test_invalid_pair_format() -> None:
    with pytest.raises(DomainValidationError):
        Symbol.from_pair("BTCUSDT")
