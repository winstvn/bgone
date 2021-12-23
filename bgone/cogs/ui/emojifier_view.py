import discord

class EmojifierView(discord.ui.View):
    
    def __init__(self, *items, timeout=180, ctx, emoji):
        self.ctx = ctx
        self.emoji = emoji
        super().__init__(*items, timeout=timeout)
        
    def disable_buttons(self):
        for child in self.children:
            child.disabled = True
            
    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(f'Was I asking if YOU wanted this emoji? No. I was asking {self.ctx.author.mention}. Now scurry off before I bgone yo bitch ass.', ephemeral=True)
            return False
        return True
        
    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
    async def yes_callback(self, button, interaction):
        self.disable_buttons()
        await interaction.response.edit_message(
            content=f'{str(self.emoji)} has been created!',
            view=self
            )
        self.stop()
    
    @discord.ui.button(label='No', style=discord.ButtonStyle.red)
    async def no_callback(self, button, interaction):
        self.disable_buttons()
        await interaction.response.edit_message(content='The emoji was not created.', view=self)
        await self.ctx.guild.delete_emoji(self.emoji, reason=f'{self.ctx.author} rejected the confirmation')
        self.stop()
        
    async def on_timeout(self):
        await self.ctx.guild.delete_emoji(self.emoji, reason='Timed out')
