import random
import pandas
from source.helpers.BaseClass import BaseClass


class DiceRoller(BaseClass):
    """Class to handle dice rolls"""

    def __init__(self):
        super().__init__("dice_rolls")
        self.comment = pandas.read_csv("source/data/comments.csv", delimiter=',')

    def roll(self, dice_num, side_num, author) -> str:
        """Command to roll dice"""

        result, percent = self.roll_calculate(dice_num, side_num)
        res = list(filter(lambda i: i < percent, self.comment.percent[::-1]))[0]
        comment = self.comment[self.comment.percent == res].sample()
        comment = comment.iloc[-1]['comment']
        self.log.info(f"Choosing comment: {comment}")

        if len(result) == 1:
            result = str(result[0])
            out = f"{comment}\n **{author}** rolled : **{result}**."
        else:
            if len(result) > 5:
                out = f"{comment}\n **{author}** rolled total of: **{sum(result)}**."
            else:
                out = f"{comment}\n **{author}** rolls: {result[0]} "
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
