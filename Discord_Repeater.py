import discord
import asyncio
import SECRETS
from discord.ext import commands
import telepot
from SECRETS import API_KEY
from telepot.aio.delegate import per_chat_id, create_open, pave_event_space
from telepot.aio.loop import MessageLoop


### DISCORD STUFF ###

# initialize discord
Client = discord.Client()
client = commands.Bot(command_prefix = "!")
client.remove_command('help')

# set discord appearance
@client.event
async def on_ready():
    print("Ready!")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name='{}'.format(SECRETS.gamename)))

# discord message handler
@client.event
async def on_message(message):
    channel = message.channel.id == SECRETS.MAIN_CH
    byBot = message.author.id == SECRETS.BOT_ID

    if not byBot and channel:
        if len(message.attachments) < 1:
            msg = "{}:\n{}".format(message.author.display_name, message.clean_content)
            await send_telegram_msg(msg)
        else:
            try:
                msg = "{}:\n{}\n".format(message.author.display_name, message.clean_content)
                for img in message.attachments:
                    msg = msg + img.url
                await send_telegram_msg(msg)
            except:
                pass

# send discord message
async def send_m(channel, m):
    if len(m) > 2000:
        m1 = m[0:2000]
        m2 = m[2000:4000]
        m3 = m[4000:]
        await asyncio.sleep(0.5)
        await channel.send(m1)
        await channel.send(m2)
        await channel.send(m3)
    else:
        await channel.trigger_typing()
        await asyncio.sleep(0.5)
        await channel.send(m)

async def send_discord_msg(msg):
    currentServer = client.get_guild(SECRETS.SERVER_ID)
    channel = currentServer.get_channel(SECRETS.MAIN_CH)
    if isinstance(msg, list):
        for m in msg:
            await send_m(channel, m)
    else:
        await send_m(channel, msg)


### TELEGRAM STUFF ###

# telegram message handler
async def on_chat_Handler(msg, current_chat):
    try:
        await send_discord_msg(msg["text"])
    except:
        await bot.sendMessage(current_chat, msg)

class MessageHandler(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)

    async def on_chat_message(self, msg):
        if msg["from"]["id"] == SECRETS.CHAT_ID:
            await on_chat_Handler(msg, SECRETS.CHAT_ID)
        else:
            pass

# send telegram message
async def send_telegram_msg(msg):
    try:
        await bot.sendMessage(SECRETS.CHAT_ID, msg)
    except:
        pass

# initialize telegram
bot = telepot.aio.DelegatorBot(API_KEY, [pave_event_space()(per_chat_id(), create_open, MessageHandler, timeout=20), ])
loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
client.run(SECRETS.TOKEN)
print('Listening ...')
loop.run_forever()
