import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import blackjack as bljack

load_dotenv()

"""
Blackjack
TODO:
- Store individual player data in MongoDB
- Add betting(currency)
- Gameplay: player and dealer hands
- Dealer logic

- Card images

- Doubles
- Splits

Poker
TODO:
---
"""

# Temp static variables
deck = []
dealerHand = []
playerHand = []
gameActive = False

# info
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
client = commands.Bot(command_prefix='.')
bot = discord.Client()

@client.event
async def on_ready():
    print("----------\nBot Online\n----------")

@client.event
async def on_message(message):
    # print(message)
    await client.process_commands(message)

@client.command(aliases=["bj"])
async def blackjack(ctx, *args):
    gameActive = True
    print("here")
    if len(args) == 0:
        await ctx.send("You must include an action!")
    else:
        action = args[0].lower()
        # try:
        #     bet = args[1]
        # except:
        #     await ctx.send("Something went wrong while placing your bet. Please try again")
        #     return 0
        
        """
        - Choice
        Player
        Dealer
        Player
        Hidden Dealer
        - Choice
        """

        if action == "new":
            await ctx.send("Starting new hand with bet ${Null}")
            bljack.fillDeck(deck)
            bljack.shuffleDeck(deck)
            gameActive = True
        elif action == "hit":
            if gameActive == False:
                await ctx.send("**You have no active blackjack hand!**\nTry ```.blackjack new BET_AMOUNT``` to start a new one!")
                return 0
            await ctx.send("user requested a hit")
            playerHand.append(bljack.getCard(deck))
            dealerHand.append(bljack.getCard(deck))
            playerHand.append(bljack.getCard(deck))
            dealerHand.append(bljack.getCard(deck))
        elif action == "stand":
            if not gameActive:
                await ctx.send("**You have no active blackjack hand!**\nTry ```.blackjack new BET_AMOUNT``` to start a new one!")
                return 0
            pass
        elif action == "split":
            if not gameActive:
                await ctx.send("**You have no active blackjack hand!**\nTry ```.blackjack new BET_AMOUNT``` to start a new one!")
                return 0
            pass
        elif action == "double":
            if not gameActive:
                await ctx.send("**You have no active blackjack hand!**\nTry ```.blackjack new BET_AMOUNT``` to start a new one!")
                return 0
            pass
        
        print(f'Dealer hand: {dealerHand}\nUser hand: {playerHand}')



client.run(TOKEN)