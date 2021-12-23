import discord

class EmojifierView(discord.ui.View):
    
    def __init__(self, *items, timeout=180, ctx, emoji):
        self.ctx = ctx
        self.emoji = emoji
        self.response = None
        super().__init__(*items, timeout=timeout)
            
    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(f'Only {self.ctx.author.mention} can respond to this.', ephemeral=True)
            return False
        return True
    
    def disable_buttons(self):
        for child in self.children:
            child.disabled = True
        
    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
    async def yes_callback(self, button, interaction):
        self.response = True
        self.disable_buttons()
        self.stop()
    
    @discord.ui.button(label='No', style=discord.ButtonStyle.red)
    async def no_callback(self, button, interaction):
        self.response = False
        self.disable_buttons()
        self.stop()
        
    async def on_timeout(self):
        self.disable_buttons()
