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

class FusionModelRatioSettings(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.height = None
        self.width = None
    @discord.ui.button(label="1:1", style=discord.ButtonStyle.blurple)
    async def one_by_one(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        self.width = 1024
        self.height = 1024
        await interaction.response.send_message("Установлен формат *1:1*")
        await interaction.message.delete()
    @discord.ui.button(label="2:3", style=discord.ButtonStyle.blurple)
    async def two_by_three(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        self.width = 640
        self.height = 960
        await interaction.response.send_message("Установлен формат *2:3*")
        await interaction.message.delete()
    @discord.ui.button(label="3:2", style=discord.ButtonStyle.blurple)
    async def three_by_two(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        self.width = 960
        self.height = 640
        await interaction.response.send_message("Установлен формат *3:2*")
        await interaction.message.delete()
    @discord.ui.button(label="3:4", style=discord.ButtonStyle.blurple)
    async def three_by_four(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        self.width = 768
        self.height = 1024
        await interaction.response.send_message("Установлен формат *3:4*")
        await interaction.message.delete()
    @discord.ui.button(label="4:3", style=discord.ButtonStyle.blurple)
    async def four_by_three(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        self.width = 1024
        self.height = 768
        await interaction.response.send_message("Установлен формат *4:3*")
        await interaction.message.delete()
    @discord.ui.button(label="16:9", style=discord.ButtonStyle.blurple)
    async def sixteen_by_nine(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        self.width = 1024
        self.height = 576
        await interaction.response.send_message("Установлен формат *16:9*")
        await interaction.message.delete()