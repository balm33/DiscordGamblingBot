from PIL import Image, ImageDraw, ImageFont
import os

cwd = os.getcwd()

def make_image(number='A', suite="spade"):
    img = Image.open(cwd + "/resources/card.png")
    d = ImageDraw.Draw(img)
    fnt = ImageFont.truetype(cwd + "/resources/Futura-Medium.ttf", 50)
    suiteImg = Image.open(cwd + f"/resources/{suite}.png").resize((32, 32))

    if suite in ["heart", "diamond"]:
        txtColor = (255, 0, 0)
    else:
        txtColor = (0, 0, 0)

    d.text((20, 10), number, fill=txtColor, font=fnt)
    

    img.paste(suiteImg, (22,75), suiteImg)
    d.text((300, 395), number, fill=txtColor, font=fnt)
    img.paste(suiteImg, (302,460), suiteImg)

    img.show()
    # img.save('img.png')
make_image()