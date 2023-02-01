import pytest
from dotenv import load_dotenv
from source.handlers.InteractionsHandler import InteractionHandler


@pytest.mark.module("InteractionHandler")
class TestInteractionHandler:
    """Class for testing InteractionHandler module"""

    load_dotenv()

    @pytest.mark.unit
    def test_interaction_handler_get_comments(self, interaction):
        """Run tests"""

        comments = interaction.get_comments()
        assert isinstance(comments, dict)

    @pytest.fixture()
    def interaction(self):
        """Fixture returning class"""

        handler = InteractionHandler()

        return handler
