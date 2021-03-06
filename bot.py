import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import blackjack as bljack
import db
import genImage

load_dotenv()
cwd = os.getcwd()

"""
Blackjack
TODO:
X Store individual player data in MongoDB
- Add betting(currency)
X Gameplay: player and dealer hands
X Dealer logic

X Card images

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

@client.command(aliases=["bal"])
async def balance(ctx):
    userId = ctx.author.id
    money = db.getMoney(userId)
    try:
        if money == None or money <= 0:
            await ctx.send("It looks like you dont have any money.\nGet some more with **.broke!**")
        else:
            await ctx.send(f'<@{userId}> has ${money}')
    except:
        await ctx.send("It looks like you dont have any money.\nGet some more with **.broke!**")

@client.command(aliases=["bankrupt"])
async def broke(ctx):
    userId = ctx.author.id
    money = db.getMoney(userId)

    try:
        if money == None or money <= 0:
            db.updateMoney(userId, 100)
            await ctx.send("Here's $100 on me!\nSpend it wisely!")
        else:
            await ctx.send(f'<@{userId}>, you have too much money to use that command!')
    except:
        db.updateMoney(userId, 100)
        await ctx.send("Here's $100 on me!\nSpend it wisely!")

@client.command(aliases=["bj"])
async def blackjack(ctx, *args):
    userId = ctx.author.id
    userName = ctx.author.name
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

        bet = userData["betAmount"]

        if action == "new":
            if len(args) < 2:
                await ctx.send("You must include an amount to bet!")
                return 0
            bet = int(args[1])
            money = db.getMoney(userId)
            if bet > money:
                await ctx.send(f"You do not have enought money in your account to make that bet!")
            else:
                db.updateMoney(userId, money - bet)
                await ctx.send(f"Starting new hand with bet ${bet}\nPlay with either **.blackjack hit** or **.blackjack stand**")

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
                    await sendImage(ctx, genImage.make_table(playerHand, dealerHand, userName, True))

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
            if action in ["hit", "h"]:
                if not gameActive:
                    await ctx.send("**You have no active blackjack hand!**\nTry ```.blackjack new BET_AMOUNT``` to start a new one!")
                    return 0
                await ctx.send(f"<@{userId}> requested a hit!")
                
                playerHand.append(bljack.getCard(deck))
                db.ins(userId, playerHand, dealerHand, gameActive, deck, bet)
                await sendImage(ctx, genImage.make_table(playerHand, dealerHand, userName, True))
            elif action in ["stand", "s"]:
                if not gameActive:
                    await ctx.send("**You have no active blackjack hand!**\nTry ```.blackjack new BET_AMOUNT``` to start a new one!")
                    return 0
                await ctx.send(f"<@{userId}> requested a stand!")
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
                if len(playerHand) == 2: # first cards
                    bet = userData["betAmount"]
                    money = db.getMoney(userId)
                    if bet > money:
                        await ctx.send(f"You do not have enought money in your account to make that bet!")
                    else:
                        db.updateMoney(userId, money - bet)
                        playerHand.append(bljack.getCard(deck))
                        db.ins(userId, playerHand, dealerHand, gameActive, deck, bet*2)
                        await ctx.send(f"<@{userId}> requested to double down!")
                        gameActive = False
            else:
                await ctx.send("That action is not recognized.")
                return 0
            
            ##############
            # Game Logic #
            ##############
            playerSum = bljack.getHandSum(playerHand)
            dealerSum = bljack.getHandSum(dealerHand)

            await ctx.send(f"<@{userId}> currently has {playerSum}")

            if playerSum == 21:
                if dealerSum != 21:
                    await sendImage(ctx, genImage.make_table(playerHand, dealerHand, userName))
                    db.updateMoney(userId, db.getMoney(userId) + (bet*2))
                    await ctx.send(f"<@{userId}> **wins ${bet*2}!**")
                    gameActive = False
                    playerHand = []
                    dealerHand = []
                    bet = None
                    db.ins(userId, playerHand, dealerHand, gameActive, deck, bet)
                else:
                    await sendImage(ctx, genImage.make_table(playerHand, dealerHand, userName))
                    db.updateMoney(userId, db.getMoney(userId) + (bet))
                    await ctx.send(f"<@{userId}> and the dealer **tie!**")
                    gameActive = False
                    playerHand = []
                    dealerHand = []
                    bet = None
                    db.ins(userId, playerHand, dealerHand, gameActive, deck, bet)
            elif dealerSum == 21 or playerSum > 21:
                await sendImage(ctx, genImage.make_table(playerHand, dealerHand, userName))
                await ctx.send(f"<@{userId}> **loses** to the dealer")
                gameActive = False
                playerHand = []
                dealerHand = []
                bet = None
                db.ins(userId, playerHand, dealerHand, gameActive, deck, bet)
            else:
                if not gameActive:
                    await sendImage(ctx, genImage.make_table(playerHand, dealerHand, userName))
                    while dealerSum < 17: # stands soft 17
                        if len(deck) <= 0: #if deck empty refill
                            bljack.fillDeck(deck)
                            bljack.shuffleDeck(deck)
                            await ctx.send("Deck shuffled!")
                        dealerHand.append(bljack.getCard(deck))
                        dealerSum = bljack.getHandSum(dealerHand)
                        db.ins(userId, playerHand, dealerHand, gameActive, deck, bet)
                    await sendImage(ctx, genImage.make_table(playerHand, dealerHand, userName))
                    if playerSum > dealerSum or dealerSum > 21: # player wins
                        db.updateMoney(userId, db.getMoney(userId) + (bet*2))
                        await ctx.send(f"<@{userId}> **wins ${bet*2}!**")
                        gameActive = False
                        playerHand = []
                        dealerHand = []
                        bet = None
                        db.ins(userId, playerHand, dealerHand, gameActive, deck, bet)
                    elif playerSum == dealerSum: # player ties
                        db.updateMoney(userId, db.getMoney(userId) + (bet))
                        await ctx.send(f"<@{userId}> and the dealer **tie!**")
                        gameActive = False
                        playerHand = []
                        dealerHand = []
                        bet = None
                        db.ins(userId, playerHand, dealerHand, gameActive, deck, bet)
                    elif dealerSum >= playerSum and dealerSum <= 21: # player loses
                        await ctx.send(f"<@{userId}> **loses** to the dealer")
                        gameActive = False
                        playerHand = []
                        dealerHand = []
                        bet = None
                        db.ins(userId, playerHand, dealerHand, gameActive, deck, bet)

@client.command()
async def test(ctx):
    await sendImage(ctx, genImage.make_table())

async def sendImage(ctx, img):
    img.save('img.png')
    await ctx.send(file=discord.File(cwd +'/img.png'))

client.run(TOKEN)