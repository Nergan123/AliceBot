import random
import json
from discord.ext import commands
from source.helpers.BaseClass import BaseClass


class DiceRoller(BaseClass, commands.Cog, name="Dice rolls"):
    """Handles all the interaction with dices"""

    def __init__(self):
        BaseClass.__init__(self, "dice_rolls")
        with open("source/data/comments.json", "r") as file:
            self.comment = json.load(file)

    @commands.command(name="roll", help='Rolls the dice. Command example "!roll 2d6"')
    async def roll(self, ctx, message) -> None:
        """Command to roll dice"""

        channel = ctx.channel.category.name
        self.log.info(f"channel: {channel}")
        if channel != "Roleplay":
            await ctx.send(
                "I'm sorry.\n"
                "This command available only in **ROLEPLAY** channels.\n"
                "For more info refer to __GITHUB__ page. Link is in my description"
            )
            return
        message = message.split("d")
        if len(message) != 2:
            await ctx.send("Please provide both numbers")
            return
        if int(message[0]) < 1 or int(message[1]) < 1:
            await ctx.send("Values should be greater than 0")
            return
        author = ctx.message.author.display_name
        out = self.roll_dice(message[0], message[1], author)

        await ctx.send(out)

    def roll_dice(self, dice_num, side_num, author) -> str:
        """Function to roll dice"""

        result, percent = self.roll_calculate(dice_num, side_num)
        res = 1000
        for key in self.comment["comments"]:
            if percent <= int(key):
                res = key
                break
        comment = self.comment["comments"][res]
        comment = random.choice(comment)
        self.log.info(f"Choosing comment: {comment}")

        if len(result) == 1:
            result = str(result[0])
            out = f"{comment}\n**{author}** rolled : **{result}**."
        else:
            if len(result) > 5:
                out = f"{comment}\n**{author}** rolled total of: **{sum(result)}**."
            else:
                out = f"{comment}\n**{author}** rolls: {result[0]} "
                for num in result[1:]:
                    out = out + f"+ {num} "

                out = out + f"= **{sum(result)}**."

        return out

    def roll_calculate(self, dice_num, side_num) -> (list, float):
        """Calculates result of the throw"""

        one_percent = (int(dice_num) * int(side_num))/100
        result = []
        for _ in range(int(dice_num)):
            result.append(random.randint(1, int(side_num)))

        if len(result) < 10:
            self.log.info(f"Rolled {dice_num} times. Results: {result}")
        else:
            self.log.info(f"Rolled {dice_num} times. Results sum: {sum(result)}")

        return result, sum(result)/one_percent
