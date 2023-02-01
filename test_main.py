import sys
import pytest
from tests.test_dice_roller import TestDiceRoller


if __name__ == "__main__":
    sys.exit(pytest.main(["-qq"], plugins=[
        TestDiceRoller()
    ]))
