import os

import discord
import file_update_discord.filetracker.filetracker as ft
import file_update_discord.filetracker.database as db
from discord.ext import commands
from file_update_discord.utils.config_reader import ConfigReader, load_env


config = ConfigReader()
botConfig = config.get("bot")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=botConfig["prefix"], intents=intents)


@bot.command()
async def ping(ctx):
    embed = discord.Embed(description=("Pong!"), colour=discord.Colour.purple())
    await ctx.send(embed=embed)


@bot.command()
async def track(ctx, url):
    try:
        dbSession = db.Database()
        if dbSession.file_exists(url):
            await ctx.send(f"URL {url} is already tracked")
            return
        else:
            file = ft.File(url, ctx.author)
            dbSession.add_file(file)
    except ValueError:
        await ctx.send(f"Invalid URL: {url}")
        return
    await ctx.send(f"Tracking {url}\nInformations {file.hash}{file.fileName}")


if __name__ == "__main__":
    load_env()
    bot.run(os.getenv("SECRET_KEY"))
