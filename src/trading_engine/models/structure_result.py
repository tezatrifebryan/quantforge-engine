from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class StructureResult:
    structure: str
    last_high: float
    last_low: float
