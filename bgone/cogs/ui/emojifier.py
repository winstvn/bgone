import re

import discord
from bgone.config import *
from bgone.exceptions import *
from bgone.utility import util
from cogs.ui.emojifier_view import EmojifierView
from discord.errors import HTTPException
from discord.ext import commands


class Emojifier(commands.Cog, name='emojifier'):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name='make-emoji')
    @commands.has_permissions(manage_emojis=True)
    async def make_emoji(self, ctx: commands.Context, name: str, url: str = '') -> None:
        """Create a server emoji with the given name.

        Args:
            name (str): An emoji name with 2 or more alphanumeric and underscore characters.
            url (str): Optional image url to create a server emoji from.
        """
        async with ctx.typing():
            try:
                url = await util.find_img_url_in_history(ctx, MSG_HISTORY_LIMIT) if url == '' else url
                existing_emoji = discord.utils.get(ctx.guild.emojis, name=name)
                
                # validate emoji name
                if not re.compile(r'^\w{2,}$').fullmatch(name):
                    await ctx.send('Emoji name must have more than 2 characters'
                                ' and contain only alphanumeric and underscore'
                                ' characters!')
                    return
                # check that the emoji doesn't already exist
                elif existing_emoji is not None:
                    await ctx.send(f'{str(existing_emoji)} already exists!')
                    return
                
                img_byte = util.get_image_btye_from_url(url)
                await ctx.guild.create_custom_emoji(
                    name=name,
                    image=img_byte,
                    reason=f'Created by {str(ctx.author)}'
                )
                
                new_emoji = discord.utils.get(ctx.guild.emojis, name=name)
                
                confirmation_view = EmojifierView(
                        timeout=EMOJIFIER_VIEW_TIMEOUT, 
                        ctx=ctx,
                        emoji=new_emoji
                        )
                
                confirmation_message = await ctx.send(
                    content=f'Emoji preview: {str(new_emoji)}\nWould you like to keep this?'
                            f'\n*Note: This menu will time out in {EMOJIFIER_VIEW_TIMEOUT} seconds.*',
                    view=confirmation_view
                    )
                
                # edit message after interaction completes
                if await confirmation_view.wait():
                    await confirmation_message.edit(
                        content='Timed out! The emoji was not created.',
                        view=None
                        )
                    await ctx.guild.delete_emoji(new_emoji, reason=f'Interaction timed out')
                else:
                    content = f'{str(new_emoji)} has been created!' if confirmation_view.response else 'The emoji was not created.'
                    await confirmation_message.edit(
                        content=content,
                        view=confirmation_view
                    )
                    if not confirmation_view.response:
                        await ctx.guild.delete_emoji(new_emoji, reason=f'{ctx.author} rejected the confirmation')
                
            except ImgNotInHistoryException as e:
                await ctx.send(e)
                
            except HTTPException as e:
                if e.code == 50035:
                    await ctx.send('Image size must be less than 256 KB!')
                else:
                    await ctx.send(e.text)
        
             
def setup(bot):
    bot.add_cog(Emojifier(bot))
