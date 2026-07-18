from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class IndicatorResult:
    values: dict[str,float]
