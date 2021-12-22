from bgone.utility import util
from bgone.utility.api_key_list import api_key_list
from bgone.config import *
from bgone.exceptions import *
from discord.ext import commands


class Removebg(commands.Cog, name='removebg'):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.key_list = api_key_list(API_KEYS, f'{API_URL}/account')

    @commands.command(name='removebg')
    async def removebg(self, ctx, url: str = ''):
        """Attempts to remove the background from an image url given as a parameter 
        or the most recently sent image.

        Args:
            url (str): A optional url containing an image to remove the background from.
        """
        
        async with ctx.typing():
            try:
                url = await util.find_img_url_in_history(ctx, MSG_HISTORY_LIMIT) if url == '' else url
                result_img = util.remove_bg(self.key_list, url)
                await ctx.send(file=util.byte_to_discord_file(result_img))
                
            except (OutOfCreditsException, 
                    RemovebgHTTPException, 
                    ImgNotInHistoryException) as e:
                await ctx.send(e)


    @commands.command(name='credits-left')
    async def credits_left(self, ctx):
        """Displays the number of free API calls left.
        """    
        await ctx.send(f'{self.key_list.total_credits} free API calls left')
        
             
def setup(bot):
    bot.add_cog(Removebg(bot))
