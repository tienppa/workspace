import os
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
import pytz
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Specify intents
intents = discord.Intents.default()
intents.members = True 
intents.presences = True 
intents.message_content = True
# Pass intents to the constructor
bot = commands.Bot(command_prefix="!", intents=intents)

# Timezone for waking up
# 5AM, adjust for desired timezone
wakeup_time = datetime.time(5, 0) 
vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
channel_id = int(os.getenv('CHANNEL_ID'))

@tasks.loop()
async def wakeup_task():
    now = datetime.datetime.now(vietnam_timezone).time()
    if now >= wakeup_time:
        print(now)
        # Replace with your channel ID
        channel = bot.get_channel(channel_id)
        await channel.send("Good morning, everyone! Time to rise and shine!")
        # Stop the loop after the first wakeup
    else:
        print("Channel not found.")
    wakeup_task.stop()  


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    # await wakeup_task()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(wakeup_task.start, 'cron', hour=wakeup_time.hour, minute=wakeup_time.minute)
    scheduler.start()

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'happy birthday' in message.content.lower():
        response = "I'm here"
        await message.channel.send(response)
    elif '/learn' in message.content.lower():
        # Get a random quote from the internet
        quote_response = requests.get("https://zenquotes.io/api/random")
        quote_data = quote_response.json()
        quote = quote_data[0]['q'] + " -" + quote_data[0]['a']
        # Get a random image from Unsplash (replace with your preferred source if needed)
        image_response = requests.get("https://source.unsplash.com/random")

        # Create an embed to display the quote and image
        embed = discord.Embed(title="Quote of the Day", description=quote, color=0x00ff00)
        embed.set_image(url=image_response.url)

        await message.channel.send(embed=embed)
    elif message.content == 'raise-exception':
        raise discord.DiscordException

bot.run(TOKEN)