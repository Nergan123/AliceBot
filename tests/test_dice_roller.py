import pytest
from source.handlers.DiceRoller import DiceRoller


@pytest.mark.dice_roller
class TestDiceRoller:
    """Class for testing Parser module"""

    @pytest.mark.unit
    def test_dice_roller_init(self, roller):
        """Run tests"""

        assert isinstance(roller.comment, dict)

    @pytest.mark.parametrize(
        "dice_num, side_num", [
            pytest.param(1, 20, marks=[pytest.mark.unit]),
            pytest.param(5, 10, marks=[pytest.mark.unit]),
            pytest.param(1000, 1000, marks=[pytest.mark.unit]),
            pytest.param(10000, 10000, marks=[pytest.mark.unit]),
            pytest.param(0, 0, marks=[pytest.mark.unit, pytest.mark.xfail()]),
            pytest.param(-1, -1, marks=[pytest.mark.unit, pytest.mark.xfail()])
        ]
    )
    def test_roll_calculate(self, roller, dice_num, side_num):
        """Testing roll calculate function"""

        max_num = dice_num * side_num
        for _ in range(50):
            out, _ = roller.roll_calculate(dice_num, side_num)

            assert 1 <= sum(out) <= max_num

    @pytest.fixture
    def roller(self):
        """Fixture returning DiceRoller class"""

        roller = DiceRoller()

        return roller
