import humanize
import discord
from discord.ext import commands

from .words import load_wordlist
from .scrabble.scoring import score_phrase
from .scrabble import scoreboard


def fence(msg: str) -> str:
    return f"```{msg}```"


class RonBot9000(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix="!")

        print("Loading wordlist...")
        self.wordlist = load_wordlist()
        print("Wordlist loaded.")

        self.add_listener(self.custom_on_message, "on_message")

    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))

    async def custom_on_message(self, message: discord.Message):
        if message.author.bot:
            return

        prefix = await self.get_prefix(message)
        if message.content.startswith(tuple(prefix)):
            return

        print(f"Message from {message.author}: {message.content}")
        points = score_phrase(message.content, wordlist=self.wordlist)
        print(f"Score: {points}")

        if points > 0:
            scoreboard.add_points(points, message=message)


ronbot9000 = RonBot9000()


@ronbot9000.command()
async def points(ctx: commands.Context):
    if not scoreboard.has_data_for_guild(ctx.guild):
        await ctx.channel.send("Nobody has said anything yet!")
        return

    top = scoreboard.get_top(5, ctx=ctx)
    asker_points = scoreboard.get_points_for_member(ctx.author)
    asker_position = scoreboard.get_points_position(asker_points, ctx=ctx)
    ordinal = humanize.ordinal(asker_position + 1)

    if top:
        top_msg = fence(
            "\n".join(
                f"{i+1}. {member.display_name}: {humanize.intcomma(points)} points"
                for i, (member, points) in enumerate(top)
            )
        )
    else:
        top_msg = "Nobody has any points yet..."

    asker_points_msg = f"<@{ctx.author.id}> you have {humanize.intcomma(asker_points)} points, "

    if asker_position == 0:
        asker_position_msg = f"putting you at the top! :tada:"
    elif asker_points == 0:
        asker_position_msg = f"get chatting!"
    else:
        asker_position_msg = f"putting you in {ordinal} position."

    await ctx.channel.send(f"Top 5:\n{top_msg}\n{asker_points_msg}{asker_position_msg}")
