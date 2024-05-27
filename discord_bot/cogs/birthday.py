import discord
from discord.ext import commands

class BirthdayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if 'happy birthday' in message.content.lower():
            response = "Happy birthday! 🎂🎉"
            await message.channel.send(response)
