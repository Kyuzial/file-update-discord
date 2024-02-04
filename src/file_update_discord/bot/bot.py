import os

import discord
import file_update_discord.filetracker.filetracker as ft
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
        file = ft.File(url, ctx.author)
    except ValueError:
        await ctx.send(f"Invalid URL: {url}")
        return
    await ctx.send(f"Tracking {url}\nInformations {file.hash}{file.fileName}")


if __name__ == "__main__":
    load_env()
    bot.run(os.getenv("SECRET_KEY"))
