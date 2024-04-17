import discord
class FusionModelStyleSettings(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.style = None
    @discord.ui.button(label="Kandinsky", style=discord.ButtonStyle.blurple)
    async def Kadinsky(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        self.style = 'KANDINSKY'
        await interaction.response.send_message("Стиль модели установлен на *Кандинский*")
        await interaction.message.delete()
    @discord.ui.button(label="Anime", style=discord.ButtonStyle.blurple)
    async def Anime(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        self.style = 'ANIME'
        await interaction.response.send_message("Стиль модели установлен на *Аниме*")
        await interaction.message.delete()
    @discord.ui.button(label="Detailed photo", style=discord.ButtonStyle.blurple)
    async def Detailed(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        self.style = 'UHD'
        await interaction.response.send_message("Стиль модели установлен на *Детальное Фото*")
        await interaction.message.delete()
    @discord.ui.button(label="No style", style=discord.ButtonStyle.blurple)
    async def Default(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        self.style = 'DEFAULT'
        await interaction.response.send_message("Стиль модели установлен на *Дефолтный*")
        await interaction.message.delete()