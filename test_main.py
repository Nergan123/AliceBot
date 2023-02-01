import sys
import pytest
from tests.test_dice_roller import TestDiceRoller
from tests.test_interaction_handler import TestInteractionHandler


if __name__ == "__main__":
    sys.exit(pytest.main(["-qq"], plugins=[
        TestDiceRoller(),
        TestInteractionHandler()
    ]))
