from quantforge.domain.enums import PositionSide


def test_position_side_values() -> None:
    assert PositionSide.LONG.value == "long"
    assert PositionSide.SHORT.value == "short"
