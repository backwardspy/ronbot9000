import typing as t
import sqlite3
from discord import guild

from discord.ext import commands
import discord

import settings

_db = None


def _get_db():
    global _db
    if _db is None:
        _db = sqlite3.connect(settings.DBNAME)
        _db.execute(
            """
            CREATE TABLE IF NOT EXISTS scoreboard (
                member_id INTEGER,
                guild_id INTEGER,
                points INTEGER,
                PRIMARY KEY (member_id, guild_id)
            )
            """
        )
    return _db


def has_data_for_guild(guild: discord.Guild) -> bool:
    db = _get_db()
    cur = db.execute(
        """
        SELECT COUNT(*) > 0 FROM scoreboard WHERE guild_id = ?
        """,
        (guild.id,),
    )
    return bool(cur.fetchone()[0])


def add_points(points: int, *, message: discord.Message) -> None:
    db = _get_db()
    db.execute(
        """
        INSERT INTO scoreboard (member_id, guild_id, points) VALUES (?, ?, ?)
        ON CONFLICT(member_id, guild_id) DO UPDATE SET points = points + excluded.points
        """,
        (message.author.id, message.guild.id, points),
    )
    db.commit()


def get_top(count: int, *, ctx: commands.Context) -> t.List[t.Tuple[discord.Member, int]]:
    db = _get_db()
    cur = db.execute(
        """
        SELECT member_id, points FROM scoreboard WHERE guild_id = ? AND points > 0 ORDER BY points DESC LIMIT ?
        """,
        (ctx.guild.id, count,),
    )
    results = cur.fetchall()
    return [(ctx.guild.get_member(member_id), points) for member_id, points in results]


def get_points_for_member(member: discord.Member) -> int:
    db = _get_db()
    cur = db.execute(
        """
        SELECT points FROM scoreboard WHERE member_id = ? AND guild_id = ? AND points > 0
        """,
        (member.id, member.guild.id),
    )

    try:
        return cur.fetchone()[0]
    except TypeError:
        return 0


def get_points_position(points: int, *, ctx: commands.Context) -> int:
    db = _get_db()
    cur = db.execute(
        """
        SELECT COUNT(*) FROM scoreboard WHERE guild_id = ? AND points > ?
        """,
        (ctx.guild.id, points,),
    )
    return cur.fetchone()[0]
