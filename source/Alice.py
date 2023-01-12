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
        commands.Bot.__init__(
            self,
            command_prefix=command_prefix,
            intents=intents
        )
        self.dice_roller = DiceRoller()
        self.add_commands()

    async def on_ready(self) -> None:
        """Log message when bot is running"""

        print(f"{self.user.name} connected to server")
        self.log.info(f"{self.user.name} connected to server")

    def add_commands(self) -> None:
        """Function to add commands"""

        @self.command(name="roll", help='Rolls the dice. Command example "!roll 2d6"')
        async def roll(ctx, message):
            """Command to roll dice"""

            message = message.split('d')
            if message[0] < 1 or message[1] < 1:
                await ctx.send("Values should be greater then 0")
                return
            author = ctx.message.author.display_name
            out = self.dice_roller.roll(message[0], message[1], author)

            await ctx.send(out)
