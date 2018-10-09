#!/usr/bin/env python
# -*- coding: utf-8 -*-

from connect4_functions import *
from NP_functions import *
from worldclock_functions import *
from math_functions import *
from notification_functions import *
from integrated_functions import *
from image_handling import *
from random import randint, choice
import calendar
import time
import discord
import discord.ext.commands as cms
from tinydb import TinyDB, Query
from tinydb.operations import add
import builtins
import datetime
from time import sleep
import glob
import time
import os

client = discord.Client()
Server = discord.Server
query = Query()

with open("token.txt") as tokenfile:
    hydroBotToken = tokenfile.readlines()[0]
    tokenfile.close()



hydroBot = cms.Bot(command_prefix="-")

hydroBot.remove_command("help")

print("Core functions initialized")

folder_init()

"""
###-Bot-commands-###
"""


@hydroBot.command(pass_context=True)
async def test(ctx):
    if notifications_closed("test", ctx.message.server, ctx.message.channel):
        return await hydroBot.say("`test` is not allowed in `" + ctx.message.channel.name + "`")
    return await hydroBot.say("test")


# Setting game-presence
@hydroBot.event
async def on_ready():
    await hydroBot.change_presence(game=discord.Game(type=1, name="SCHICK HYDROBOT!"))


"""
on_message:
Awarding exp and litcoins for messages sent.
"""


@hydroBot.event
async def on_message(message):
    # Make exception for bot-messages:
    if message.author == discord.User.bot:
        return
    time_since_epoch = time.time()
    litcoinlist = TinyDB("litcoin/LITCOIN" + message.server.id + ".json")
    levellist = TinyDB("level/LEVEL" + message.server.id + ".json")
    author = message.author.id

    if not levellist.contains(query["user"] == author):
        levellist.insert(
            {"user": author, "level": 1, "exp": 0, "exp_range_min": 15, "exp_range_max": 25, "time": time_since_epoch})
    exp = randint(levellist.search(query["user"] == author)[0]["exp_range_min"],
                  levellist.search(query["user"] == author)[0]["exp_range_max"])

    if not litcoinlist.contains(query["user"] == author):
        litcoinlist.insert({"user": author, "balance": 500, "time": time_since_epoch, "gain": 1})
    elif litcoinlist.search((query["user"] == author) & (query["time"] < time_since_epoch - 60)):
        litcoinlist.update(add("balance", (litcoinlist.search(query["user"] == author)[0]["gain"])),
                           query["user"] == author)

    if levellist.search(query["user"] == author)[0]["time"] < time_since_epoch - 60:
        levellist.update(add("exp", exp), query["user"] == author)
        levellist.update({"time": time_since_epoch}, query["user"] == author)
    if levelup(levellist.search(query["user"] == author)[0]["exp"],
               levellist.search(query["user"] == author)[0]["level"]):
        levellist.update(add("level", 1), query["user"] == author)
        levellist.update({"exp": 0}, query["user"] == author)
        levelup_message = "`Level_BETA`: " + message.author.name + " leveled up to level `" + str(
            levellist.search(query["user"] == author)[0]["level"]) + "`"
        litcoinlist.update({"gain": levellist.search(query["user"] == author)[0]["level"]}, query["user"] == author)
        levelup_message += ", their litcoin gain per message has increased to `" + str(
            litcoinlist.search(query["user"] == author)[0]["gain"]) + "`"
        litcoinlist.update(add("balance", round((levellist.search(query["user"] == author)[0]["level"] ** 1.2) * 100)),
                           query["user"] == author)
        levelup_message += " and `" + str(round((levellist.search(query["user"] == author)[0][
                                                     "level"] ** 1.2) * 100)) + "` LitCoins have been transfered to their account :moneybag:"
        levelup_message += " :clap::clap:"
        if not notifications_closed("level", message.server, message.channel):
            await hydroBot.send_message(message.channel, levelup_message)
    await hydroBot.process_commands(message)


"""
Litcoin:
Currency commands.
"""
@hydroBot.command(pass_context=True)
async def litcoin(ctx, arg1="", arg2="", arg3=""):
    if notifications_closed("litcoin", ctx.message.server, ctx.message.channel):
        return await hydroBot.say("`litcoin` is not allowed in `" + ctx.message.channel.name + "`")

    litcoinlist = TinyDB("litcoin/LITCOIN" + ctx.message.server.id + ".json")
    levellist = TinyDB("level/LEVEL" + ctx.message.server.id + ".json")
    balance = litcoinlist.search(query["user"] == ctx.message.author.id)[0]["balance"]
    author = ctx.message.author

    if arg1 == "":
        return await hydroBot.say(
            "Welcome to LitCoin. The best of the best of hydrocurrencies. You get `1` litcoin for each message you send in a channel in the server (If the bot is allowed in the channel Kappa) with a `30` second cooldown.\nThese are the commands that you can use to manage your account:\n`!litcoin balance`: check your current balance of LitCoins\n`!litcoin gamba <amount> <odds>`: gamble you LitCoins for a chance of more. standard bet is 10, standard odds are 2 (1/odds)\n`!litcoin transfer <user.id> <amount>`: Transfer a specified amount of litcoin to another member\nThanks for using LitCoin, more features are implemented over time")


    elif arg1 == "balance":
        if notifications_closed("balance", ctx.message.server, ctx.message.channel):
            return await hydroBot.say("`balance` is not allowed in `" + ctx.message.channel.name + "`")
        if balance is None:
            return await hydroBot.say(
                author.name + " has not yet set up their account, to set up an account, type a regular message in chat and wait a few seconds.")
        return await hydroBot.say("The balance of " + author.name + " is `" + str(balance) + "` :moneybag:")


    elif arg1 == "gamba":
        if notifications_closed("gamba", ctx.message.server, ctx.message.channel):
            return await hydroBot.say("`gamba` is not allowed in `" + ctx.message.channel.name + "`")

        if ctx.message.channel == discord.utils.get(ctx.message.server.channels, name="general"):
            return await hydroBot.say("To avoid spam, gamba is not to be used in #general")

        if arg2 == "":
            bet = 10
        else:
            try:
                bet = int(arg2)
                if not bet == round(bet) or not bet > 0:
                    bet = 10
                if balance < bet:
                    return await hydroBot.say("Sorry but you can't do a gamble of this size.")
            except:
                bet = 10
                await hydroBot.say("Instructions unclear, dick stuck in coin slot, and bet set to default (10)")
        if arg3 == "":
            odds = 2
        else:
            try:
                odds = int(arg3)
                if odds < 1:
                    odds = 2
                if not odds == round(odds):
                    odds = 2
            except:
                odds = 2
                await hydroBot.say("Instructions unclear, dick stuck in coin slot, and odds set to default (2)")
        pull = randint(1, odds)
        litcoinlist.update(add("balance", - bet), query["user"] == author.id)
        if pull == 1:
            litcoinlist.update(add("balance", bet * odds), query["user"] == author.id)
            return await hydroBot.say(author.name + " just won `" + str(
                bet * odds - bet) + "` LitCoins in the gamba-suite with the odds: `" + str(
                odds - 1) + "` to 1 :pound: :pound: :pound:")
        else:
            return await hydroBot.say(author.name + " lost `" + str(bet) + "` on their bet with the odds: `" + str(
                odds - 1) + "` to 1 :confused:")


    elif arg1 == "shop":
        if notifications_closed("shop", ctx.message.server, ctx.message.channel):
            return await hydroBot.say("`shop` is not allowed in `" + ctx.message.channel.name + "`")

        if arg2 == "":
            return await hydroBot.say("You can buy the following in the shop:\n`exp_minimum " + str(round((((
                                                                                                            levellist.search(
                                                                                                                query[
                                                                                                                    "user"] == author.id)[
                                                                                                                0][
                                                                                                                "exp_range_min"]) - 14) ** 1.3) * 500)) + " LitCoins`: Increase the minimum exp-gain per message by 1. Default is 15.\n`exp_maximum " + str(
                round((((levellist.search(query["user"] == ctx.message.author.id)[0][
                             "exp_range_max"]) - 24) ** 1.3) * 500)) + " LitCoins`: Increase the maximum exp-gain per message by 1. Default is 25.\n`joke_submit " + '"<joke>"' + " 5000 Litcoins`: Add a joke to the 'usersubmitted' joke-genre")

        if arg2 == "exp_minimum":
            if levellist.search(query["user"] == author.id)[0]["exp_range_min"] == \
                    levellist.search(query["user"] == author.id)[0]["exp_range_max"]:
                return await hydroBot.say("Sorry, but your minimum xp-award range must be lower than your maximum")
            cost = round(
                (((levellist.search(query["user"] == ctx.message.author.id)[0]["exp_range_min"]) - 14) ** 1.3) * 500)
            await hydroBot.say("It will cost you `" + str(
                cost) + "` LitCoins to upgrade your minimum exp reward per message from `" + str(
                levellist.search(query["user"] == author.id)[0]["exp_range_min"]) + "` to `" + str(
                levellist.search(query["user"] == ctx.message.author.id)[0][
                    "exp_range_min"] + 1) + "` . If you wanna purchase, type `purchase`, else type `reject` :dollar::pound:")
            if litcoinlist.search(query["user"] == author.id)[0]["balance"] < cost:
                return await hydroBot.say(author.name + " cannot afford this upgrade :confused:")
            msg = await hydroBot.wait_for_message(author=ctx.message.author)
            if msg.content.startswith("purchase"):
                levellist.update(add("exp_range_min", 1), query["user"] == author.id)
                litcoinlist.update(add("balance", -cost), query["user"] == author.id)
                return await hydroBot.say(author.name + " has purchased `exp-minimum-threshold upgrade` for `" + str(
                    cost) + "` LitCoins. DAYUM")
            elif msg.content.startswith("reject"):
                return await hydroBot.say(author.name + " has rejected the purchase")
            else:
                return await hydroBot.say(author.name + ", i didn't understand that. Closing thread...")

        elif arg2 == "exp_maximum":
            cost = round(((levellist.search(query["user"] == author.id)[0]["exp_range_max"] - 24) ** 1.3) * 500)
            await hydroBot.say("It will cost you `" + str(
                cost) + "` LitCoins to upgrade your maximum exp reward per message from `" + str(
                levellist.search(query["user"] == author.id)[0]["exp_range_max"]) + "` to `" + str(
                levellist.search(query["user"] == ctx.message.author.id)[0][
                    "exp_range_max"] + 1) + "` . If you wanna purchase, type `purchase`, else type `reject` :dollar::pound:")
            if litcoinlist.search(query["user"] == author.id)[0]["balance"] < cost:
                return await hydroBot.say(author.name + " cannot afford this upgrade :confused:")
            msg = await hydroBot.wait_for_message(author=author)
            if msg.content.startswith("purchase"):
                levellist.update(add("exp_range_max", 1), query["user"] == author.id)
                litcoinlist.update(add("balance", -cost), query["user"] == author.id)
                return await hydroBot.say(author.name + " has purchased `exp-maximum-threshold upgrade` for `" + str(
                    cost) + "` LitCoins. DAYUM")
            elif msg.content.startswith("reject"):
                return await hydroBot.say(author.name + " has rejected the purchase")
            else:
                return await hydroBot.say(author.name + ", i didn't understand that. Closing thread...")
        else:
            return await hydroBot.say("I am sorry but we don't sell that here")
    else:
        return await hydroBot.say("I didn't quite understand what you meant by " + arg1)


"""
        elif arg1 == "transfer":
            if notifications_closed("transfer", ctx.message.server, ctx.message.channel):
                return await hydroBot.say("`transfer` is not allowed in `" + ctx.message.channel.name + "`")

            if arg2 is None:
                return await hydroBot.say("You cannot transfer LitCoin to the aether")
            try:
                if int(arg3) < 0:
                    return await hydroBot.say("What kind of bank do you think i am?")
                if arg3 == "" or type(int(arg3)) != int:
                    return await hydroBot.say("You have to select a whole number to transfer")
            except:
                return await hydroBot.say("You have to select a whole number to transfer")
            if balance < int(arg3):
                return await hydroBot.say("You don't have enough LitCoins to do a transfer of that caliber")
            try:
                litcoinlist.search(query["user"] == arg2)
            except:
                return await hydroBot.say("2nd argument must be an @user tag")
            litcoinlist.update(add("balance", - int(arg3)), query["user"] == author.id)
            litcoinlist.update(add("balance", int(arg3)), query["user"] == arg2.id)
            return await hydroBot.say(author.name + " just transfered `" + arg3 + "` LitCoins to " + arg2.name)
"""

"""
--- NOTIFICATIONS ---
The system that turns alerts from every command on and off.
Can only be accessed by admins.
"""


@hydroBot.command(pass_context=True)
async def notifications(ctx, command="", option=""):
    if not (is_admin(ctx.message.author) or ctx.message.author.id == "166953638961479681"):
        return hydroBot.say("This message can only be accessed by admins")
    channel = ctx.message.channel
    server = ctx.message.server
    notificationlist = TinyDB("notifications/NOTIFICATIONS" + server.id + ".json")
    commandlist = ["test", "litcoin", "level", "gamba", "balance", "shop", "transfer", "music", "meme", "metome", "itsretarded", "itstime", "classnote", "headache", "firstword"]
    notifications = notification_get(server, channel)
    if command == "view":
        return await hydroBot.say(notificationlist.all())
    if command not in commandlist and command != "":
        return await hydroBot.say(command + " is not a command that can be blocked")
    if option not in ["block", "allow", ""]:
        return await hydroBot.say("Bad argument `" + option + "` not recognized")
    if command == "":
        if notifications == []:
            return await hydroBot.say("There are no blocked commands in this channel")
        outputmessage = "Currently blocked commands in #" + channel.name + ":\n`"
        for i in notifications:
            outputmessage += i + "`, `"
        outputmessage = outputmessage[:-3]
        return await hydroBot.say(outputmessage)
    if command not in notifications:
        if option == "block":
            notification_block(server, channel, command)
            return await hydroBot.say("the command `" + command + "` has been blocked in `#" + channel.name + "`")
        await hydroBot.say(
            "The command `" + command + "` is currently allowed in `#" + channel.name + "`. Type `-notifications " + command + " block` to prevent it from being used")
    else:
        if option == "allow":
            notification_allow(server, channel, command)
            return await hydroBot.say("the command `" + command + "` has been allowed in `#" + channel.name + "`")
        await hydroBot.say(
            "The command `" + command + "` is currently blocked in `#" + channel.name + "`. Type `-notifications " + command + " allow` to enable its use")


@hydroBot.command(pass_context=True)
async def meme(ctx, template="", *args):
    if notifications_closed("meme", ctx.message.server, ctx.message.channel):
        return await hydroBot.say("`meme` is not allowed in `" + ctx.message.channel.name + "`")

    for i in args:
        if len(i) > 200:
            return await hydroBot.say("Text cannot be longer than 200 characters")

    if template in ["metome", "mealsome", "mtm"]:
        if notifications_closed("metome", ctx.message.server, ctx.message.channel):
            return await hydroBot.say("`metome` is not allowed in `" + ctx.message.channel.name + "`")
        image = mealsome_function(args[0], args[1])
        await hydroBot.send_file(ctx.message.channel, "imagesaving/" + image + ".png")
        os.remove("imagesaving/" + image + ".png")
        return None

    elif template in ["itsretarded", "retarded", "ir"]:
        if notifications_closed("itsretarded", ctx.message.server, ctx.message.channel):
            return await hydroBot.say("`itsretarded` is not allowed in `" + ctx.message.channel.name + "`")
        text1 = ""
        for i in args:
            text1 += i + " "
        image = itsretarded_function(text1)
        await hydroBot.send_file(ctx.message.channel, "imagesaving/" + image + ".png")
        os.remove("imagesaving/" + image + ".png")
        return None

    elif template in ["headache", "stress", "ha"]:
        if notifications_closed("headache", ctx.message.server, ctx.message.channel):
            return await hydroBot.say("`headache` is not allowed in `" + ctx.message.channel.name + "`")
        text1 = ""
        for i in args:
            text1 += i + " "
        image = headache_function(text1)
        await hydroBot.send_file(ctx.message.channel, "imagesaving/" + image + ".png")
        os.remove("imagesaving/" + image + ".png")
        return None

    elif template in ["note", "classnote", "cheatsheet", "cn"]:
        if notifications_closed("classnote", ctx.message.server, ctx.message.channel):
            return await hydroBot.say("`classnote` is not allowed in `" + ctx.message.channel.name + "`")
        text1 = ""
        for i in args:
            text1 += i + " "
        image = classnote_function(text1)
        await hydroBot.send_file(ctx.message.channel, "imagesaving/" + image + ".png")
        os.remove("imagesaving/" + image + ".png")
        return None

    elif template in ["itstime", "goofy", "goofytime", "gt", "it"]:
        if notifications_closed("itstime", ctx.message.server, ctx.message.channel):
            return await hydroBot.say("`itstime` is not allowed in `" + ctx.message.channel.name + "`")
        image = itstime_function(args[0], args[1])
        await hydroBot.send_file(ctx.message.channel, "imagesaving/" + image + ".png")
        os.remove("imagesaving/" + image + ".png")

    elif template in ["firstword", "firstwords", "fw"]:
        if notifications_closed("firstword", ctx.message.server, ctx.message.channel):
            return await hydroBot.say("`firstword` is not allowed in `" + ctx.message.channel.name + "`")
        text1 = ""
        for i in args:
            text1 += i + " "
        image = firstword_function(text1)
        await hydroBot.send_file(ctx.message.channel, "imagesaving/" + image + ".png")
        os.remove("imagesaving/" + image + ".png")

    else:
        return await hydroBot.say("`" + template + "` is not an indexed meme template")


@hydroBot.command(pass_context=True)
async def hdb(ctx, arg1="", arg2="", arg3=""):
    litcoinlist = TinyDB("litcoin/LITCOIN" + ctx.message.server.id + ".json")
    levellist = TinyDB("level/LEVEL" + ctx.message.server.id + ".json")
    if ctx.message.author != Server.get_member(ctx.message.server, "166953638961479681"):
        return await hydroBot.say("Debugging is not for plebs. This is serious business.")
    elif arg1 == "say":
        return await hydroBot.say(arg2)

    elif arg1 == "lc_p":
        litcoinlist.purge_tables()

    elif arg1 == "lc_s":
        user = arg2
        balance = arg3
        litcoinlist.update({"balance": int(balance)}, query["user"] == user)
        return await hydroBot.say(
            "Set the balance of " + Server.get_member(ctx.message.server, user).name + "'s account to `" + str(
                balance) + "`")
    return


@hydroBot.command()
async def hydrohelp(type):
    if type == "":
        return await hydroBot.say("You can find all my commands here: <http://julianbrandt.dk/hydrobot/commands>")


@hydroBot.command()
async def fancy(type, *args):
    inputtext = ""
    for i in args:
        inputtext += i + " "

    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

    fancytexts = {
        "gothic": "𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅յշՅկՏճԴՑգօ",
        "cicles": "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ①②③④⑤⑥⑦⑧⑨⓪",
        "box": "𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡𝟘",
        "bold_serif": "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗𝟎",
        "bold_sansserif": "𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕1234567890",
        "special": "ᗩᗷᑕᗪEᖴGᕼIᒍKᒪᗰᑎOᑭᑫᖇᔕTᑌᐯᗯ᙭YᘔᗩᗷᑕᗪEᖴGᕼIᒍKᒪᗰᑎOᑭᑫᖇᔕTᑌᐯᗯ᙭Yᘔ1234567890",
        "upside_down": "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz∀qƆpƎℲפHIſʞ˥WNOԀQɹS┴∩ΛMX⅄ZƖᄅƐㄣϛ9ㄥ860"
    }

    if type not in fancytexts:
        return await hydroBot.say("Error: Not able to convert to type `" + type + "`")

    outputtext = ""
    for i in inputtext:
        if i in alphabet:
            outputtext += fancytexts[type][alphabet.index(i)]
        else:
            outputtext += i

    return await hydroBot.say(outputtext)


@hydroBot.command()
async def math(*args):
    calcualtion = math_function(*args)
    if calcualtion is None:
        return await hydroBot.say("Error in calculation. Check your input")
    return await hydroBot.say(calcualtion)

"""
@hydroBot.command(pass_context=True)
async def plot(ctx, style, *args):
    if style in ["point", "line", "dash"]:
        display = plot_dataset(style, *args)
        await hydroBot.send_file(ctx.message.channel, display)
        os.remove(display)
    else:
        return await hydroBot.say("`Error in input`")
"""
"""
@hydroBot.command(pass_context=True)
async def plotf(ctx, *args):
    equation = args[0]
    try:
        minrange = args[1]
    except:
        minrange = "-5"
    try:
        maxrange = args[2]
    except:
        if int(minrange) > 0:
            minrange = str(-int(minrange))
        maxrange = str(-int(minrange))
    try:
        color = args[3]
    except:
        color = "red"
    try:
        linestyle = args[4]
    except:
        linestyle = "solid"

    display = input_func(equation, minrange, maxrange)

    if display == "error":
        return await hydroBot.say("`Error in input`")
    await hydroBot.send_file(ctx.message.channel, display)
    os.remove(display)
"""

@hydroBot.command()
async def timezone(zone, commandtype=None):
    time_in_zone = timezone_current(zone, commandtype)
    return await hydroBot.say(time_in_zone)


@hydroBot.command(pass_context=True)
async def play(ctx, link=""):
    if not hydroBot.is_voice_connected(ctx.message.server):
        voice = await hydroBot.join_voice_channel(ctx.message.author.voice_channel)
    else:
        voice = hydroBot.voice_client_in(ctx.message.server)
    player = await voice.create_ytdl_player(link)
    player.start()


@hydroBot.command()
async def help():
    return await hydroBot.say("You can find the Hydro Bot docs here: http://julianbrandt.dk/hydrobot/commands")


@hydroBot.command(pass_context=True)
async def c(ctx, img):
    image = contrast_function(img)
    await hydroBot.send_file(ctx.message.channel, "imagesaving/" + image + ".png")
    os.remove("imagesaving/" + image + ".png")


@hydroBot.command(pass_context=True)
async def connect4(ctx):
    p1 = ctx.message.author
    mention = ctx.message.mentions
    p2 = " "
    for user in mention:
        p2 = user

    if p2 == " ":
        return await hydroBot.say("You must mention the user you want to play against")

    await hydroBot.say(p1.name + " has challenged " + p2.name + " to a game of connect four (type 'connect4' to accept)")
    response = " "
    timeOfInit = calendar.timegm(time.gmtime())
    while response != "connect4" and calendar.timegm(time.gmtime()) < timeOfInit + 60:
        response = await hydroBot.wait_for_message(channel=ctx.message.channel, author=p2)
        response = response.content
    if response != "connect4":
        return await hydroBot.say(p2.name + " has rejected the challenge")
    else:
        coinflip = randint(0, 1)
        starter = [p1, p2][coinflip]
        if coinflip == 0:
            second = p2
        else:
            second = p1

        startmessage = await hydroBot.say("Game started. Flipping coin to determine starting player :clock12:")
        clocklist = [":clock3:", ":clock6:", ":clock9:", ":clock12:"]
        for i in range(0, 4):
            await hydroBot.edit_message(startmessage, "Game started. Flipping coin to determine starting player " + clocklist[i])
        await hydroBot.edit_message(startmessage, "The starting player will be " + starter.name)

    board = [[0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0]]

    winner = c4_check(board)

    boardmessage2 = await hydroBot.say("Begin!")
    while winner == 0:
        await hydroBot.delete_message(boardmessage2)
        boardmessage1 = await hydroBot.say(starter.name + ", it's your turn\n \n" + print_board(board))
        move = await hydroBot.wait_for_message(channel=ctx.message.channel, author=starter)
        move = move.content
        move_possible = False
        while not move_possible:
            if move == "quit":
                return await hydroBot.say(starter.name + " has quit the game\n:clap: " + second.name + " wins! :clap:")
            if move not in ["1", "2", "3", "4", "5", "6", "7"]:
                await hydroBot.say("You have to input a number between 1 and 7")
                move = await hydroBot.wait_for_message(channel=ctx.message.channel, author=starter)
                move = move.content
            if move in ["1", "2", "3", "4", "5", "6", "7"]:
                move = int(move) - 1
                moved = False
                for i in range(5, -1, -1):
                    if board[move][i] == 0:
                        move_possible = True
                        board[move][i] = 1
                        moved = True
                        break

                previousmove = move
                while not moved:
                    await hydroBot.say("This column is full")
                    move = await hydroBot.wait_for_message(channel=ctx.message.channel, author=starter)
                    move = move.content
                    if previousmove != move:
                        moved = True

        winner = c4_check(board)

        if not winner:
            await hydroBot.delete_message(boardmessage1)
            boardmessage2 = await hydroBot.say(second.name + ", it's your turn\n \n" + print_board(board))
            move = await hydroBot.wait_for_message(channel=ctx.message.channel, author=second)
            move = move.content
            move_possible = False
            while not move_possible:
                if move == "quit":
                    return await hydroBot.say(second.name + " has quit the game\n:clap: " + starter.name + " wins! :clap:")
                if move not in ["1", "2", "3", "4", "5", "6", "7"]:
                    await hydroBot.say("You have to input a number between 1 and 7")
                    move = await hydroBot.wait_for_message(channel=ctx.message.channel, author=second)
                    move = move.content
                if move in ["1", "2", "3", "4", "5", "6", "7"]:
                    move = int(move) - 1
                    moved = False
                    for i in range(5, -1, -1):
                        if board[move][i] == 0:
                            move_possible = True
                            board[move][i] = 2
                            moved = True
                            break

                    previousmove = move
                    while not moved:
                        await hydroBot.say("This column is full")
                        move = await hydroBot.wait_for_message(channel=ctx.message.channel, author=second)
                        move = move.content
                        if move != previousmove:
                            moved = True

            winner = c4_check(board)

    if winner == 'draw':
        return await hydroBot.say("It's a draw. There is no winner\n \n" + print_board(board))

    if winner == 1:
        winner = starter
    else:
        winner = second

    return await hydroBot.say(":clap: " + winner.name + " wins the game! :clap:\n \n" + print_board(board))


@hydroBot.command(pass_context=True)
async def clocktest(ctx):
    startmessage = await hydroBot.say("Game started. Flipping coin to determine starting player :clock12:")
    clocklist = [":clock3:", ":clock6:", ":clock9:", ":clock12:"]
    for i in range(0, 4):
        await hydroBot.edit_message(startmessage, "Game started. Flipping coin to determine starting player " + clocklist[i])



print("Commands initialized. Running bot...")
hydroBot.run(hydroBotToken)
