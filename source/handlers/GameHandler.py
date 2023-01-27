import os
import json
import random
import asyncio
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from discord.ext import commands
from source.helpers.BaseClass import BaseClass


class GameHandler(BaseClass, commands.Cog, name="Games"):
    """Functionality to play some games"""

    SERIALIZABLE_FIELDS = [
        "state",
        "players",
        "order",
        "turn",
    ]

    def __init__(self):
        BaseClass.__init__(self, "game_handler_data")
        self.state = 0
        self.players = {}
        self.order = []
        self.turn = 0
        self.load_state()
        with open("source/data/game/start_comments.json", "r") as data:
            self.start_comments = json.loads(data.read())
        with open("source/data/game/game_comments.json", "r") as data:
            self.roll_comments = json.loads(data.read())
        self.endings = ["Y"]

        load_dotenv()
        key = os.getenv('KEY')
        fernet = Fernet(key)
        with open("source/data/game/outcomes_encr.json", "r") as encr_data:
            encrypted = encr_data.read()
        decrypted = fernet.decrypt(encrypted)
        self.outcomes = json.loads(decrypted)

    @commands.command(name="start_game", help="Starts a dice game. Rules are in GitHub")
    async def start_game(self, ctx):
        """Starts a dice game"""

        if ctx.channel.category.name.lower() != "roleplay":
            await ctx.send(
                "I'm sorry.\n"
                "This command available only in **ROLEPLAY** channels.\n"
                "For more info refer to __GITHUB__ page. Link is in my description"
            )
            return

        if self.state == 0:
            self.state = 1
            self.log.info(f"User {ctx.author.name} starts a game.")
            self.save_state()
            comment = random.choice(self.start_comments["phrase"])
            await ctx.send(
                f"{comment}\n"
                f"Who is participating?\n\n"
                f"Use __start_game__ command when all players are connected\n"
                f"Use __connect__ to enter the game\n"
                f"If you reach minimum score of 1 just bet 1. Your bet will be skipped"
            )
            await ctx.send("===================================================")
        elif self.state == 1:
            self.state = 2
            self.save_state()
            self.log.info("Starting **initiative** stage")
            await ctx.send("===================================================")
            await ctx.send("Registered users: ")

            message = "```\n"
            for name in self.players:
                message = message + f"{name}\t| Height: {self.players[name]['height']}\n"

            message = message + "```"
            await ctx.send(message)

            for name in self.players:
                await ctx.send(f"User {name} your initiative is: "
                               f"{self.players[name]['initiative']}")
            await ctx.send("===================================================")

            self.sort_queue()
            message = "Turns:\n" \
                      "```\n"
            for name in self.order:
                message = message + f"{name} with initiative = {self.players[name]['initiative']}\n"
            message = message + "```"
            await ctx.send(message)
            await ctx.send(f"Your turn **{self.order[0]}**")

    @commands.command(name="end_game", help="Ends the running game")
    async def end_game(self, ctx):
        """Ends current game"""

        if ctx.channel.category.name.lower() != "roleplay":
            await ctx.send(
                "I'm sorry.\n"
                "This command available only in **ROLEPLAY** channels.\n"
                "For more info refer to __GITHUB__ page. Link is in my description"
            )
            return

        if self.state != 0:
            self.state = 0
            self.players = {}
            self.order = []
            self.turn = 0
            self.log.info("Terminating running game")
            self.save_state()
            await ctx.send("===================================================")
            await ctx.send(f"User **{ctx.author.display_name}** terminated the game")
            await ctx.send("===================================================")
        else:
            await ctx.send("No games are running at the moment")
            self.log.info("No games are running at the moment")

    @commands.command(name="connect", help="Registers a participant in the game")
    async def connect(self, ctx):
        """Connects a player to the game"""

        if ctx.channel.category.name.lower() != "roleplay":
            await ctx.send(
                "I'm sorry.\n"
                "This command available only in **ROLEPLAY** channels.\n"
                "For more info refer to __GITHUB__ page. Link is in my description"
            )
            return

        if self.state == 0:
            await ctx.send("Sorry, but you have to first **start** the game")
            return
        if self.state >= 2:
            await ctx.send("Sorry, the game has already started")
            return

        if ctx.author.display_name not in self.players:
            self.players[ctx.author.display_name] = {}
            self.players[ctx.author.display_name]["height"] = 6
            self.players[ctx.author.display_name]["initiative"] = random.randint(1, 20)
            self.log.info(f"Adding {ctx.author.display_name}")
            self.save_state()
            await ctx.send(f"User **{ctx.author.display_name}** has joined the game")
        else:
            self.log.info(f"{ctx.author.display_name} already registered")
            await ctx.send("You are already registered")

    @commands.command(name="bet", help="Takes a height unit as input. "
                                       "Rolls a 1d6 for you and acts according to the result")
    async def bet(self, ctx, message):
        """Makes a bet and acts accordingly"""

        if ctx.channel.category.name.lower() != "roleplay":
            await ctx.send(
                "I'm sorry.\n"
                "This command available only in **ROLEPLAY** channels.\n"
                "For more info refer to __GITHUB__ page. Link is in my description"
            )
            return

        if self.state != 2:
            await ctx.send("Sorry it is not time to bet yet.")
            self.log.info(f"Current session {self.state} expected 2")
            return

        current_player = self.order[self.turn]
        if ctx.author.display_name != current_player:
            await ctx.send(f"It is turn of {current_player}")
            return
        try:
            bet = int(message)
            if bet < 1:
                await ctx.send("Bet should be more than 0")
                return
            if self.players[current_player]["height"] < bet:
                await ctx.send("Bet is too high. Try something else")
                return
        except ValueError as e:
            self.log.warning(f"User {ctx.author.display_name} input invalid\n{e}")
            await ctx.send("Your bet is in the wrong format")
            return

        if self.players[current_player]["height"] <= 1:
            await ctx.send("Skipping since minimum height reached")
            self.turn += 1
            if self.turn >= len(self.order):
                self.turn = 0
                message = "```\n"
                for name in self.players:
                    message = message + f"{name}\t| Height: {self.players[name]['height']}\n"

                message = message + "```"
                await ctx.send(message)
            return

        roll = random.randint(1, 6)
        if roll == 1:
            comment = random.choice(self.roll_comments["1"])
        elif roll == 6:
            comment = random.choice(self.roll_comments["4"])
        elif roll % 2 == 0 and roll != 6:
            comment = random.choice(self.roll_comments["2"])
        else:
            comment = random.choice(self.roll_comments["3"])

        await ctx.send(f"{comment}\nYour roll is **{roll}**")

        if roll == 1:
            for name in self.players.keys():
                self.players[name]["height"] -= round(bet / 2)
                if name == current_player:
                    self.players[name]["height"] -= round(bet / 2)
            await ctx.send(f"Your height is **{self.players[current_player]['height']}**")
            outcome = await self.check_win_conditions(ctx)
            self.save_state()
            if outcome:
                return

        elif roll == 6:
            self.players[current_player]["height"] += bet * 2
            await ctx.send(f"Your height is **{self.players[current_player]['height']}**")
            outcome = await self.check_win_conditions(ctx)
            self.save_state()
            if outcome:
                return

        elif roll % 2 == 0 and roll != 6:
            self.players[current_player]["height"] += bet
            await ctx.send(f"Your height is **{self.players[current_player]['height']}**")
            outcome = await self.check_win_conditions(ctx)
            self.save_state()
            if outcome:
                return

        else:
            for name in self.players.keys():
                self.players[name]["height"] += bet

            self.players[current_player]["height"] -= round(bet * 2)
            await ctx.send(f"Your height is **{self.players[current_player]['height']}**")
            outcome = await self.check_win_conditions(ctx)
            self.save_state()
            if outcome:
                return

        self.turn += 1
        if self.turn >= len(self.order):
            self.turn = 0
            message = "```\n"
            for name in self.players:
                message = message + f"{name}\t| Height: {self.players[name]['height']}\n"

            message = message + "```"
            await ctx.send(message)

        self.log.info(f"Current turn: {self.turn}")
        self.log.info(f"Current order: {self.order}")

        await ctx.send(f"Now it is turn of **{self.order[self.turn]}**")

    @commands.command(name="get_height", help="Returns a list of players heights")
    async def get_height(self, ctx):
        """Returns a height list"""

        if ctx.channel.category.name.lower() != "roleplay":
            await ctx.send(
                "I'm sorry.\n"
                "This command available only in **ROLEPLAY** channels.\n"
                "For more info refer to __GITHUB__ page. Link is in my description"
            )
            return

        if self.state != 2:
            await ctx.send("Sorry the game is not running yet.")
            self.log.info(f"Current session {self.state} expected 2")
            return

        message = "```\n"
        for name in self.players:
            message = message + f"{name}\t\t| Height: {self.players[name]['height']}\n"

        message = message + "```"
        await ctx.send(message)
        return

    def sort_queue(self):
        """Sorts an initiative queue"""

        initiatives = []
        names = []
        for name in self.players.keys():
            initiatives.append(self.players[name]["initiative"])
            names.append(name)

        _, names_new = zip(*sorted(zip(initiatives, names)))
        self.order = list(names_new[::-1])
        self.save_state()
        self.log.info(f"Final order:\n{self.order}")

    async def check_win_conditions(self, ctx):
        """Checks if condition for victory is met"""

        for name in self.players.keys():
            if self.players[name]["height"] >= 5000:
                await ctx.send(f"We have a winner! It is {name}.\n"
                               f"Please choose the fate for the ones who have lost")
                if self.state != 0:
                    self.state = 0
                    self.players = {}
                    self.order = []
                    self.turn = 0
                    self.log.info("Terminating running game")
                    self.save_state()
                return True

        winner = []
        for name in self.players.keys():
            if self.players[name]["height"] <= 1:
                self.players[name]["height"] = 1
            else:
                winner.append(name)

        if len(winner) == 1 and len(self.players.keys()) > 1:
            await ctx.send(f"We have a winner! It is {winner[0]}.\n"
                           f"Please choose the fate for the ones who have lost")
            if self.state != 0:
                self.state = 0
                self.players = {}
                self.order = []
                self.turn = 0
                self.log.info("Terminating running game")
                self.save_state()
            return True

        if len(winner) < 1:
            await ctx.send("Oh my. I guess I am the winner.\nAbout your fate...\nGive me a second")
            async with ctx.typing():
                await asyncio.sleep(20)
            personality = random.choice(self.endings)
            await ctx.send(self.outcomes[personality]["intro"])
            await ctx.send(self.outcomes[personality]["gif"])
            for name in self.players.keys():
                async with ctx.typing():
                    await asyncio.sleep(20)
                await ctx.send(f"**{name}** your fate:")
                await ctx.send(random.choice(self.outcomes[personality]["comments"]))
            if self.state != 0:
                self.state = 0
                self.players = {}
                self.order = []
                self.turn = 0
                self.log.info("Terminating running game")
                self.save_state()
            return True
        return False
