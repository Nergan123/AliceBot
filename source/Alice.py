import discord
from discord.ext import commands
from source.helpers.BaseClass import BaseClass
from source.handlers.DiceRoller import DiceRoller


class Alice(commands.Bot, BaseClass):
    """Alice bot main class"""

    def __init__(self, command_prefix):
        BaseClass.__init__(self, "alice_data")
        intents = discord.Intents.default()
        intents.message_content = True
        commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents)

    async def on_ready(self) -> None:
        """Log message when bot is running"""

        await self.add_cog(DiceRoller())
        print(f"{self.user.name} connected to server")
        self.log.info(f"{self.user.name} connected to server")
