from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from random import randint
import sys
import numpy as np


def splitLine(font, text, width):
    textconvert = text
    returntext = ""
    while textconvert:
        if (font.getsize(textconvert)[0]) < width:
            returntext += textconvert
            break
        for i in range(len(textconvert), 0, -1):
            if (font.getsize(textconvert[:i])[0]) < width:
                if ' ' not in textconvert[:i]:
                    returntext += textconvert[:i] + "-\n"
                    textconvert = textconvert[i:]
                else:
                    for l in range(i, 0, -1):
                        if textconvert[l] == ' ':
                            returntext += textconvert[:l]
                            returntext += "\n"
                            textconvert = textconvert[l + 1:]
                            break
                break
    if returntext[-3] == "-":
        returntext = returntext[:-3]
    return returntext


def mealsome_function(text1="", text2=""):
    img = Image.open("imagelibrary/mealsome.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 24)

    returntext = splitLine(font, text1, 400)
    returntext2 = splitLine(font, text2, 350)

    draw.text((60, 0),returntext,(0,0,0),font=font)
    draw.text((120, 100),returntext2,(0,0,0),font=font)

    imagename = str(randint(1000000000,9999999999))

    img.save("imagesaving/" + imagename + '.png')
    return imagename


def itsretarded_function(text1=""):
    ypos = 56
    if 60 > len(text1) > 30:
        ypos = 30
    elif len(text1) >= 60:
        ypos = 3
    img = Image.open("imagelibrary/itsretarded.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 20)

    returntext = splitLine(font, text1, 220)

    draw.text((253, ypos), returntext, (0, 0, 0), font=font)

    imagename = str(randint(1000000000, 9999999999))

    img.save("imagesaving/" + imagename + '.png')
    return imagename


def headache_function(text1=""):
    returntext = text1
    ypos = 0
    if len(text1) < 8:
        font1_size = 54
        xpos = 0
    elif len(text1) < 14:
        font1_size = 54
        xpos = 60
    elif len(text1) < 14:
        font1_size = 54
        xpos = (len(text1)-10)*16
    else:
        font1_size = 46 - (len(text1)-16)
        xpos = (len(text1)-15)*10
        if len(text1) < 20:
            xpos += 50
        ypos += 46-font1_size

    img = Image.open("imagelibrary/headache.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("impact.ttf", font1_size)
    draw.text((390-xpos, 490+ypos), returntext, (0, 0, 0), font=font)

    imagename = str(randint(1000000000, 9999999999))

    img.save("imagesaving/" + imagename + '.png')
    return imagename


def itstime_function(text1="", text2=""):
    ypos = 60
    ypos2 = 380
    font1_size = 36
    font2_size = 24

    img = Image.open("imagelibrary/itstime.png")
    draw = ImageDraw.Draw(img)
    font1 = ImageFont.truetype("arial.ttf", font1_size)
    font2 = ImageFont.truetype("arial.ttf", font2_size)

    returntext = splitLine(font1, text1, 200)
    returntext2 = splitLine(font2, text2, 110)

    draw.text((60, ypos), returntext, (0, 0, 0), font=font1)
    draw.text((95, ypos2), returntext2, (0, 0, 0), font=font2)

    imagename = str(randint(1000000000, 9999999999))

    img.save("imagesaving/" + imagename + '.png')
    return imagename


def classnote_function(text1=""):
    ypos = 0
    if len(text1) <= 8:
        font1_size = 36
        ypos = 20
    else:
        font1_size = 24

    img = Image.open("imagelibrary/classnote.png")
    font = ImageFont.truetype("arial.ttf", font1_size)
    img = img.rotate(30, expand=True)
    draw = ImageDraw.Draw(img)

    returntext = splitLine(font, text1, 175)

    draw.text((585, 545+ypos), returntext, (0, 0, 0), font=font)
    img = img.rotate(-30)
    img = img.crop((128, 138, 888, 858))

    imagename = str(randint(1000000000, 9999999999))

    img.save("imagesaving/" + imagename + '.png')
    return imagename


def firstword_function(text1=""):
    stuttertext = text1[0] + "..." + text1[0] + "..."

    if len(text1) <= 10:
        ypos = 0
    elif len(text1) <= 20:
        ypos = 40
    else:
        ypos = 95

    img = Image.open("imagelibrary/firstword.png")
    font = ImageFont.truetype("comic.ttf", 60)
    draw = ImageDraw.Draw(img)

    returntext = splitLine(font, text1, 500)

    draw.text((100, 30), stuttertext, (0, 0, 0), font=font)
    draw.text((100, 580 - ypos), returntext, (0, 0, 0), font=font)

    imagename = str(randint(1000000000, 9999999999))

    img.save("imagesaving/" + imagename + '.png')
    return imagename


def nutbutton_function(text1=""):
    ypos = 0
    if len(text1) <= 5:
        font1_size = 72
        ypos = 15
    else:
        font1_size = 48

    img = Image.open("imagelibrary/nutbutton.jpg")
    font = ImageFont.truetype("arial.ttf", font1_size)
    img = img.rotate(10, expand=True)
    draw = ImageDraw.Draw(img)

    returntext = splitLine(font, text1, 175)

    draw.text((133, 300+ypos), returntext, (255, 255, 255), font=font)
    img = img.rotate(-10)

    imagename = str(randint(1000000000, 9999999999))
    img = img.crop((33, 47, 600, 446))

    img.save("imagesaving/" + imagename + '.png')
    return imagename


def swu_uok_function(text1="", text2=""):
    xpos1 = 100
    xpos2 = 100
    ypos1 = 0
    ypos2 = 0
    if len(text1) > 8:
        xpos1 = 20
    if len(text2) > 8:
        xpos2 = 20

    if len(text1) > 20:
        ypos1 = -80
    if len(text2) > 20:
        ypos2 = -80

    img = Image.open("imagelibrary/swu_uok.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 36)

    returntext = splitLine(font, text1, 220)
    returntext2 = splitLine(font, text2, 220)

    draw.text((xpos1, 102 + ypos1), returntext, (0, 0, 0), font=font)
    draw.text((xpos2, 380 + ypos2), returntext2, (0, 0, 0), font=font)

    imagename = str(randint(1000000000, 9999999999))

    img.save("imagesaving/" + imagename + '.png')
    return imagename
