import discord
from discord.ext import commands
from source.helpers.BaseClass import BaseClass
from source.handlers.DiceRoller import DiceRoller
from source.handlers.GameHandler import GameHandler
from source.handlers.InteractionsHandler import InteractionHandler


class Alice(commands.Bot, BaseClass):
    """Alice bot main class"""

    def __init__(self, command_prefix):
        BaseClass.__init__(self, "alice_data")
        intents = discord.Intents.default()
        intents.message_content = True
        commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents)
        self.dice_roller = DiceRoller()
        self.game_handler = GameHandler()
        self.interaction_handler = InteractionHandler()

    async def on_ready(self) -> None:
        """Log message when bot is running"""

        await self.add_cog(self.dice_roller)
        await self.add_cog(self.game_handler)
        await self.add_cog(self.interaction_handler)
        print(f"{self.user.name} connected to server")
        self.log.info(f"{self.user.name} connected to server")
