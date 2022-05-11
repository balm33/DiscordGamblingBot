import discord
from discord.ext import commands

"""
Blackjack
TODO:
- Store individual player data in MongoDB
- Add betting(currency)
- Gameplay: player and dealer hands
- Dealer logic

- Doubles
- Splits

Poker
TODO:
---
"""

# info
TOKEN = "XXXX"
client = commands.Bot(command_prefix='.')
bot = discord.Client()

@client.event
async def on_ready():
    print("----------\nBot Online\n----------")

@client.event
async def on_message(message):
    print(message)

client.run(TOKEN)