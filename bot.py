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
    bet = None
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
            try:
                deck = userData["deck"]
                dealerHand = []
                playerHand = []
                if len(deck) <= 0: #if deck empty refill
                    bljack.fillDeck(deck)
                    bljack.shuffleDeck(deck)
                    await ctx.send("Deck shuffled!")
                gameActive = True
                db.ins(userId, playerHand, dealerHand, gameActive, deck, bet)
                userData = db.findById(userId)
            except:
                await ctx.send("Error: something went wrong")
        else:
            deck = userData["deck"]
            playerHand = userData["userCards"]
            dealerHand = userData["dealerCards"]
            gameActive = userData["isHandActive"]

            if len(deck) <= 0: #if deck empty refill
                    bljack.fillDeck(deck)
                    bljack.shuffleDeck(deck)
                    await ctx.send("Deck shuffled!")
            
            #################
            # Player Action #
            #################
            if action == "hit":
                if not gameActive:
                    await ctx.send("**You have no active blackjack hand!**\nTry ```.blackjack new BET_AMOUNT``` to start a new one!")
                    return 0
                await ctx.send("user requested a hit")
                
                if len(playerHand) == 0: # first turn
                    if len(deck) < 4: #if deck empty refill
                        bljack.fillDeck(deck)
                        bljack.shuffleDeck(deck)
                        await ctx.send("Deck shuffled!")
                    playerHand.append(bljack.getCard(deck))
                    dealerHand.append(bljack.getCard(deck))
                    playerHand.append(bljack.getCard(deck))
                    dealerHand.append(bljack.getCard(deck))
                    db.ins(userId, playerHand, dealerHand, gameActive, deck, bet)
                else:
                    playerHand.append(bljack.getCard(deck))
                    db.ins(userId, playerHand, dealerHand, gameActive, deck, bet)

            elif action == "stand":
                if not gameActive:
                    await ctx.send("**You have no active blackjack hand!**\nTry ```.blackjack new BET_AMOUNT``` to start a new one!")
                    return 0
                await ctx.send("user requested a stand")
                db.ins(userId, playerHand, dealerHand, gameActive, deck, bet)
                gameActive = False
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
            else:
                await ctx.send("That action is not recognized.")
                return 0
            
            ##############
            # Game Logic #
            ##############
            playerSum = bljack.getHandSum(playerHand)
            dealerSum = bljack.getHandSum(dealerHand)

            if playerSum == 21:
                if dealerSum != 21:
                    await ctx.send("player wins")
                    gameActive = False
                    playerHand = []
                    dealerHand = []
                    bet = None
                    db.ins(userId, playerHand, dealerHand, gameActive, deck, bet)
                else:
                    await ctx.send("player ties")
                    gameActive = False
                    playerHand = []
                    dealerHand = []
                    bet = None
                    db.ins(userId, playerHand, dealerHand, gameActive, deck, bet)
            elif dealerSum == 21:
                await ctx.send("player loses")
                gameActive = False
                playerHand = []
                dealerHand = []
                bet = None
                db.ins(userId, playerHand, dealerHand, gameActive, deck, bet)
            else:
                if not gameActive:
                    while dealerSum < 17: # stands soft 17
                        if len(deck) <= 0: #if deck empty refill
                            bljack.fillDeck(deck)
                            bljack.shuffleDeck(deck)
                            await ctx.send("Deck shuffled!")
                        dealerHand.append(bljack.getCard(deck))
                        dealerSum = bljack.getHandSum(dealerHand)
                        db.ins(userId, playerHand, dealerHand, gameActive, deck, bet)
                    if playerSum > dealerSum: # player wins
                        await ctx.send("player wins")
                        gameActive = False
                        playerHand = []
                        dealerHand = []
                        bet = None
                        db.ins(userId, playerHand, dealerHand, gameActive, deck, bet)
                    elif dealerSum >= playerSum and dealerSum <= 21: # player loses
                        await ctx.send("player loses")
                        gameActive = False
                        playerHand = []
                        dealerHand = []
                        bet = None
                        db.ins(userId, playerHand, dealerHand, gameActive, deck, bet)
                    elif playerSum == dealerSum: # player ties
                        await ctx.send("player ties")
                        gameActive = False
                        playerHand = []
                        dealerHand = []
                        bet = None
                        db.ins(userId, playerHand, dealerHand, gameActive, deck, bet)
            print(f'Dealer hand: {dealerHand}\nUser hand: {playerHand}')
            print(f'Dealer sum: {dealerSum}\nUser sum: {playerSum}')



client.run(TOKEN)