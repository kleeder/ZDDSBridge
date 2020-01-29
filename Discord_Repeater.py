import discord
import time
import asyncio
import random
import SECRETS
from discord.ext import commands
import sys
import time
import telepot
from SECRETS import API_KEY

Client = discord.Client()
client = commands.Bot(command_prefix = "!")
client.remove_command('help')

@client.event
async def on_message(message):
    # check if the message was sent in a private chat
    privateChat = message.channel.name == None

    # check in which channel the message was sent
    # debug = message.channel.id == "535069981688463376"
    owouwuqwq = message.channel.id == "535950032898228245"
    # statsChannel = message.channel.id == "537938898345656331"

    # check if the message author is botti himself
    byBot = message.author.bot

    if not byBot and owouwuqwq:
        pass

    elif not byBot and not privateChat:

        # time to check for commands
        if len(message.attachments) < 1:
            # print(message.content)
            msg = "{} @ {} \n{}".format(message.author, message.channel, message.content)
            send_telegram_msg(msg)
        else:
            # print(message.attachments[0]['url'])
            try:
                msg = "{} @ {} \n{}".format(message.author, message.channel, message.content)
                send_telegram_msg(msg)
                for img in message.attachments:
                    send_telegram_msg(img['url'])
                    # print(img.url)
            except:
                pass


def send_telegram_msg(msg):
    bot = telepot.Bot(API_KEY)
    bot.sendMessage(123456789, msg)


# initialize
client.run(SECRETS.TOKEN)
