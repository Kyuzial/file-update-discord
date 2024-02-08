import os

import discord
import file_update_discord.filetracker.database as db
import file_update_discord.filetracker.filetracker as ft
from discord.ext import commands, tasks
from file_update_discord.utils.config_reader import ConfigReader, load_env

config = ConfigReader()
botConfig = config.get("bot")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=botConfig["prefix"], intents=intents)

dbSession = db.Database()


@bot.command()
async def ping(ctx):
    embed = discord.Embed(description=("Pong!"), colour=discord.Colour.purple())
    await ctx.send(embed=embed)


@bot.command()
async def track(ctx, url):
    try:
        if dbSession.file_exists(url):
            await ctx.send(f"URL {url} is already tracked")
            return
        else:
            file = ft.File(url, ctx.author.id)
            dbSession.add_file(file)
    except ValueError:
        await ctx.send(f"Invalid URL: {url}")
        return
    await ctx.send(f"Tracking {url}\nInformations {file.hash}")


@bot.command()
async def untrack(ctx, url):
    try:
        if ctx.author.id != dbSession.get_author(url):
            await ctx.send(f"URL {url} is not tracked by you")
            return
        else:
            dbSession.remove_file(url)
            await ctx.send(f"URL {url} is no longer tracked")
    except ValueError as exc:
        await ctx.send(exc)
        return


@tasks.loop(seconds=3600)
async def refresh_all_files_hash():
    updated = dbSession.update_all_files_hash()
    for item in updated:
        print(item)
        await bot.get_user(item[3]).send(
            f"File {item[2]} has been updated at {item[1]}\nNew hash: {item[0]}"
        )
    dbSession.clear_updates()


@bot.event
async def on_ready():
    refresh_all_files_hash.start()


if __name__ == "__main__":
    load_env()
    secret_key = os.getenv("SECRET_KEY")
    if secret_key is not None:
        bot.run(secret_key)
    else:
        print("SECRET_KEY not found in environment variables")
