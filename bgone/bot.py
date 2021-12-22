from discord.ext import commands

from config import *
from exceptions import *

bot = commands.Bot(command_prefix='!')

            
def load_cogs(cogs_to_load: list) -> None:
    for cog in cogs_to_load:
        bot.load_extension(cog)


if __name__ == '__main__':
    load_cogs(COGS)
    bot.run(TOKEN)
