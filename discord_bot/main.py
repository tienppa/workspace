import discord
from discord.ext import commands
from dotenv import load_dotenv
import config
from utils import scheduler
from cogs.greetings import GreetingsCog
from cogs.birthday import BirthdayCog
from cogs.quotes import QuotesCog 

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.presences = True 
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Load cogs
bot.add_cog(GreetingsCog(bot))
bot.add_cog(BirthdayCog(bot))
bot.add_cog(QuotesCog(bot))

@bot.event
async def on_ready():
    await bot.sync_commands()
    
    print(f'{bot.user} has connected to Discord!')

scheduler.schedule_wakeup_task(bot, config.CHANNEL_ID)  

bot.run(config.DISCORD_TOKEN)
