import random
import json
import boto3
from discord.ext import commands
from source.helpers.BaseClass import BaseClass


class InteractionHandler(BaseClass, commands.Cog, name="Interactions"):
    """Handles interactions in chat"""

    def __init__(self):
        BaseClass.__init__(self, "interaction_handler")

    @commands.command(
        name="interact",
        help="Chooses interaction from list. "
        "Put 'P' in the end for personal category",
    )
    async def interact(self, ctx, interaction="", category="g") -> None:
        """Chooses random interaction from list"""

        self.log.info(f"Input: {interaction}, category: {category}")
        channel = ctx.channel.category.name
        self.log.info(f"channel: {channel}")
        if channel.lower() != "roleplay":
            await ctx.send(
                "I'm sorry.\n"
                "This command available only in **ROLEPLAY** channels.\n"
                "For more info refer to __GITHUB__ page. Link is in my description"
            )
            return

        interaction = interaction.lower()
        category = category.lower()
        state = self.get_comments()
        user_id = str(ctx.author.id)
        if self.check_banned_id(user_id):
            await ctx.send("You can't use this command")
            return

        if category != "g":
            output = self.choose_from_user(user_id, state, interaction)
        else:
            output = self.choose_from_general(state, interaction)

        await ctx.send(f"{ctx.author.display_name}: {output}")

    @commands.command(name="dev")
    async def dev_command(self, ctx):
        """Command for dev only"""

        if ctx.author.id != 278900472679628800:
            return
        await ctx.message.delete()
        self.log.info(ctx.message.content)
        await ctx.send(ctx.message.content[5:])

    @commands.command(name="add_personal", help="Adds your comment to category")
    async def add_personal(self, ctx, category, *args) -> None:
        """Adds personal comment to category"""

        comment = ""
        for arg in args:
            comment = comment + f" {arg}"
        channel = ctx.channel.category.name
        self.log.info(f"channel: {channel}")
        if channel.lower() != "roleplay":
            await ctx.send(
                "I'm sorry.\n"
                "This command available only in **ROLEPLAY** channels.\n"
                "For more info refer to __GITHUB__ page. Link is in my description"
            )
            return

        user_id = str(ctx.author.id)
        if self.check_banned_id(user_id):
            await ctx.send("You can't use this command")
            return

        if category == "":
            await ctx.send("Please provide category")
            return

        if comment == "":
            await ctx.send("Please provide comment")
            return

        self.log.info(f"Provided category: {category}, comment: {comment}")
        state = self.get_comments()
        category = category.lower()
        category_list = state["General"].keys()
        if category not in category_list:
            await ctx.send(
                f"Can't find category: {category}\n"
                f"Existing categories: {list(category_list)}"
            )
            return

        self.log.info(f"Adding comment: {comment}\n" f"By {ctx.author.display_name}")
        if user_id not in state.keys():
            state[user_id] = {}
            state[user_id][category] = []

        if category not in state[user_id].keys():
            state[user_id][category] = []

        comments = state[user_id][category]
        comments.append(comment)
        state[user_id][category] = comments
        self.set_comments(state)
        await ctx.send("Added")

    def choose_from_user(self, user_id, state, interaction) -> str:
        """Chooses from user category"""

        if user_id not in state.keys():
            self.log.warning("User category not found")
            return (
                "Your category doesn't exist.\n"
                "You can create one using *add_personal*"
            )

        if interaction not in state[user_id].keys():
            self.log.warning(
                f"Can't find {interaction}"
                f"Existing categories: {list(state['General'].keys())}"
            )
            return (
                f"Category not found.\n"
                f"Existing categories: {list(state[user_id].keys())}"
            )

        comment = random.choice(state[user_id][interaction])
        self.log.info(f"Choosing comment: {comment}")

        return comment

    def choose_from_general(self, state, interaction) -> str:
        """Chooses a string from general category"""

        if interaction not in state["General"].keys():
            self.log.warning(
                f"Can't find {interaction}"
                f"Existing categories: {list(state['General'].keys())}"
            )
            return (
                f"Category not found.\n"
                f"Existing categories: {list(state['General'].keys())}"
            )

        comment = random.choice(state["General"][interaction])
        self.log.info(f"Choosing comment: {comment}")

        return comment

    def get_comments(self) -> dict:
        """Gets comments from bucket"""

        self.log.info("Getting comments database")
        s3 = boto3.client("s3")
        s3_response = s3.get_object(
            Bucket=self.state_bucket, Key="interaction_comments.json"
        )
        state_json = s3_response["Body"].read()
        state = json.loads(state_json)

        return state

    def set_comments(self, state) -> None:
        """Uploads comment to bucket"""

        self.log.info("Setting comments database")
        s3 = boto3.resource("s3")
        remote_object = s3.Object(self.state_bucket, "interaction_comments.json")
        remote_object.put(Body=(bytes(json.dumps(state).encode("UTF-8"))))
