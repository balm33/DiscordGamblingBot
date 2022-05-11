import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import blackjack as bljack
import db

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

# info
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
client = commands.Bot(command_prefix='.')
bot = discord.Client()

@client.event
async def on_ready():
    print("----------\nBot Online\n----------")

@client.event
async def on_message(message):
    # print(message.author.id)
    await client.process_commands(message)

@client.command(aliases=["bj"])
async def blackjack(ctx, *args):
    userId = ctx.author.id
    userData = db.findById(userId)
    gameActive = False
    
    if len(args) == 0:
        await ctx.send("You must include an action!")
    else:
        action = args[0].lower()
        
        """
        - Choice
        Player
        Dealer
        Player
        Hidden Dealer
        - Choice
        """

        # creates adds empty data to database for user
        if(userData == None):
            # dict = {
            #     "userId": userId,
            #     "userCards": [],
            #     "dealerCards": [],
            #     "isHandActive": False,
            #     "deck": [],
            #     "betAmount": None
            # }
            db.ins(userId, [], [], False, [], None)
            userData = db.findById(userId)

        if action == "new":
            if len(args) < 2:
                await ctx.send("You must include an amount to bet!")
                return 0
            await ctx.send("Starting new hand with bet ${None}")
            # try:
            deck = userData["deck"]
            dealerHand = []
            playerHand = []
            if len(deck) <= 0: #if deck empty refill
                bljack.fillDeck(deck)
                bljack.shuffleDeck(deck)
            gameActive = True
            db.ins(userId, playerHand, dealerHand, gameActive, deck, None) # must fix: add bet
            userData = db.findById(userId)
            # except:
            #     await ctx.send("Error: something went wrong")
        elif action == "hit":
            if not gameActive:
                await ctx.send("**You have no active blackjack hand!**\nTry ```.blackjack new BET_AMOUNT``` to start a new one!")
                return 0
            await ctx.send("user requested a hit")
            # playerHand.append(bljack.getCard(deck))
            # dealerHand.append(bljack.getCard(deck))
            # playerHand.append(bljack.getCard(deck))
            # dealerHand.append(bljack.getCard(deck))
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