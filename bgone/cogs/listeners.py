import discord
from discord.ext import commands


class Listeners(commands.Cog, name='listeners'):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')
    

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        raise error
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        cleaned_message = message.content.strip().lower()
        jar_emoji = discord.utils.get(message.guild.emojis, name='jar3')
        
        if cleaned_message == 'come':
            if jar_emoji:
                await message.add_reaction(jar_emoji)
            else:
                await message.add_reaction('💦')
        
             
def setup(bot):
    bot.add_cog(Listeners(bot))
