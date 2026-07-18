"""
Trading symbol value object.
"""

from __future__ import annotations

from dataclasses import dataclass

from quantforge.domain.exceptions import DomainValidationError


@dataclass(frozen=True, slots=True)
class Symbol:
    """
    Immutable market symbol.
    """

    base: str
    quote: str

    def __post_init__(self) -> None:
        """
        Validate and normalize base and quote assets.
        """

        base = self.base.strip().upper()
        quote = self.quote.strip().upper()

        if not base:
            raise DomainValidationError("Symbol base asset is required.")

        if not quote:
            raise DomainValidationError("Symbol quote asset is required.")

        if base == quote:
            raise DomainValidationError(
                "Symbol base and quote assets must be different."
            )

        object.__setattr__(self, "base", base)
        object.__setattr__(self, "quote", quote)

    @classmethod
    def from_pair(cls, pair: str) -> "Symbol":
        """
        Create a symbol from a BASE/QUOTE pair.
        """

        parts = pair.split("/")

        if len(parts) != 2:
            raise DomainValidationError("Symbol pair must use BASE/QUOTE format.")

        return cls(parts[0], parts[1])

    def __str__(self) -> str:
        return f"{self.base}/{self.quote}"
