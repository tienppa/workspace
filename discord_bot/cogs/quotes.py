import discord
from discord.ext import commands
import requests

class QuotesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # Check for /learn in the message content
        if message.content.lower() == "/learn": 
            await self.send_quote(message.channel)

    async def send_quote(self, channel):
        quote_response = requests.get("https://zenquotes.io/api/random")
        quote_data = quote_response.json()
        quote = quote_data[0]['q'] + " -" + quote_data[0]['a']

        image_response = requests.get("https://source.unsplash.com/random")

        embed = discord.Embed(title="Quote of the Day", description=quote, color=0x00ff00)
        embed.set_image(url=image_response.url)
        
        await channel.send(embed=embed)
