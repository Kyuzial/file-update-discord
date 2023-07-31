import os

import discord
from discord.ext import commands
from utils.config_reader import ConfigReader, load_env

config = ConfigReader()
botConfig = config.get("bot")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=botConfig["prefix"], intents=intents)


@bot.command()
async def ping(ctx):
    embed = discord.Embed(description=(f"Pong!"), colour=discord.Colour.purple())
    await ctx.send(embed=embed)


if __name__ == "__main__":
    load_env()
    bot.run(os.getenv("SECRET_KEY"))
