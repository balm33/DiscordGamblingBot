from PIL import Image, ImageDraw, ImageFont
import os

cwd = os.getcwd()

def make_image(date="2020 09 21", day="A"):
    img = Image.open(cwd + "images/.png")
    
    img.show()
    # img.save('img.png')
make_image()