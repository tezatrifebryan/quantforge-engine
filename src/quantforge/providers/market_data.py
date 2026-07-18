"""
Market data provider contracts and adapters.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from typing import Protocol

from quantforge.domain.value_objects import Candle, Price, Symbol, Timeframe, Volume
from quantforge.providers.exceptions import ProviderError

MILLISECONDS_PER_SECOND = 1_000
OHLCV_COLUMN_COUNT = 6
TIMESTAMP_INDEX = 0
OPEN_INDEX = 1
HIGH_INDEX = 2
LOW_INDEX = 3
CLOSE_INDEX = 4
VOLUME_INDEX = 5

OhlcvScalar = Decimal | int | float | str
RawOhlcvRow = Sequence[OhlcvScalar]


class MarketDataProvider(Protocol):
    """
    Contract for market data providers.
    """

    def fetch_candles(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        since: datetime | None = None,
        limit: int | None = None,
    ) -> tuple[Candle, ...]:
        """
        Fetch candles for a symbol and timeframe.
        """


class OhlcvClient(Protocol):
    """
    Minimal client contract compatible with CCXT fetch_ohlcv.
    """

    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str,
        since: int | None = None,
        limit: int | None = None,
    ) -> Sequence[RawOhlcvRow]:
        """
        Fetch raw OHLCV rows.
        """


class CcxtMarketDataProvider:
    """
    Market data provider backed by a CCXT-compatible client.
    """

    def __init__(self, client: OhlcvClient) -> None:
        self._client = client

    def fetch_candles(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        since: datetime | None = None,
        limit: int | None = None,
    ) -> tuple[Candle, ...]:
        """
        Fetch raw OHLCV data and normalize it into candles.
        """

        if limit is not None and limit <= 0:
            raise ProviderError("Candle fetch limit must be greater than zero.")

        raw_rows = self._client.fetch_ohlcv(
            symbol=str(symbol),
            timeframe=str(timeframe),
            since=_datetime_to_milliseconds(since),
            limit=limit,
        )

        return tuple(
            _row_to_candle(
                row=row,
                symbol=symbol,
                timeframe=timeframe,
            )
            for row in raw_rows
        )


def _datetime_to_milliseconds(value: datetime | None) -> int | None:
    if value is None:
        return None

    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)

    return int(value.timestamp() * MILLISECONDS_PER_SECOND)


def _row_to_candle(
    row: RawOhlcvRow,
    symbol: Symbol,
    timeframe: Timeframe,
) -> Candle:
    if len(row) != OHLCV_COLUMN_COUNT:
        raise ProviderError("OHLCV row must contain six values.")

    timestamp_ms = _integer(row[TIMESTAMP_INDEX], "timestamp")

    return Candle(
        symbol=symbol,
        timeframe=timeframe,
        timestamp=datetime.fromtimestamp(
            timestamp_ms / MILLISECONDS_PER_SECOND,
            tz=UTC,
        ),
        open_price=Price(_decimal(row[OPEN_INDEX], "open")),
        high_price=Price(_decimal(row[HIGH_INDEX], "high")),
        low_price=Price(_decimal(row[LOW_INDEX], "low")),
        close_price=Price(_decimal(row[CLOSE_INDEX], "close")),
        volume=Volume(_decimal(row[VOLUME_INDEX], "volume")),
    )


def _integer(value: OhlcvScalar, field_name: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise ProviderError(f"Invalid OHLCV {field_name}.") from exc


def _decimal(value: OhlcvScalar, field_name: str) -> Decimal:
    try:
        return Decimal(str(value))
    except InvalidOperation as exc:
        raise ProviderError(f"Invalid OHLCV {field_name}.") from exc
