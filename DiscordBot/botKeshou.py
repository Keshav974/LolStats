import discord
from discord.ext import commands

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("ok")

@client.command()
async def fébour(ctx):
    await ctx.send("Nicolas")

@client.command()
async def stats(ctx):
    with open("mon_fichier.txt", "r") as f:
        message = f.read()

    await ctx.send(message)

client.run("Token")
