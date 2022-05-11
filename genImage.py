from PIL import Image, ImageDraw, ImageFont
import os

cwd = os.getcwd()

def make_image(number='A', suite="spades", turnOne=False):
    img = Image.open(cwd + "/resources/card.png")
    d = ImageDraw.Draw(img)
    fnt = ImageFont.truetype(cwd + "/resources/Futura-Medium.ttf", 50)
    suiteImg = Image.open(cwd + f"/resources/{suite}.png").resize((32, 32))

    if suite in ["hearts", "diamonds"]:
        txtColor = (255, 0, 0)
    else:
        txtColor = (0, 0, 0)

    if not turnOne:
        d.text((20, 10), number, fill=txtColor, font=fnt)
        img.paste(suiteImg, (22,75), suiteImg)
        d.text((300, 395), number, fill=txtColor, font=fnt)
        img.paste(suiteImg, (302,460), suiteImg)

    # img.show()
    # img.save('img.png')
    return img

def make_table(userHand, dealerHand, userName, turnOne=False):
    img = Image.new("RGB", (600,400), (115, 120, 128))
    d = ImageDraw.Draw(img)
    fnt = ImageFont.truetype(cwd + "/resources/Futura-Medium.ttf", 25)
    fnt2 = ImageFont.truetype(cwd + "/resources/Futura-Medium.ttf", 15)

    d.text((10, 10), userName, fill=(255, 255, 255), font=fnt2)

    d.text((225, 10), "Dealer Cards", fill=(255, 255, 255), font=fnt)
    if turnOne:
        img2 = make_image(dealerHand[0][0], dealerHand[0][1]).resize((int(362*.25), int(512*.25)))
        img.paste(img2, (95*0+5, 50), img2)
        img2 = make_image(dealerHand[1][0], dealerHand[1][1], True).resize((int(362*.25), int(512*.25)))
        img.paste(img2, (95*1+5, 50), img2)
    else:
        for i in range(len(dealerHand)):
            img2 = make_image(dealerHand[i][0], dealerHand[i][1]).resize((int(362*.25), int(512*.25)))
            img.paste(img2, (95*i+5, 50), img2)

    d.text((225, 210), "Player Cards", fill=(255, 255, 255), font=fnt)
    for i in range(len(userHand)):
        img2 = make_image(userHand[i][0], userHand[i][1]).resize((int(362*.25), int(512*.25)))
        img.paste(img2, (95*i+5, 250), img2)

    # img.show()
    return img
# make_table([['4', 'clubs'], ['5', 'diamonds']], [['4', 'clubs'], ['5', 'diamonds']])