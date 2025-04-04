import discord

class zodiac_settings(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.zodiac_sign = None
    @discord.ui.select(
        placeholder = "Выбери свой знак зодиака",
        options = [
            discord.SelectOption(
                label="Овен",
            ),
            discord.SelectOption(
                label="Телец",
            ),
            discord.SelectOption(
                label="Близнецы",
            ),
            discord.SelectOption(
                label="Рак",
            ),
            discord.SelectOption(
                label="Лев",
            ),
            discord.SelectOption(
                label="Дева",
            ),
            discord.SelectOption(
                label="Весы",
            ),
            discord.SelectOption(
                label="Скорпион",
            ),
            discord.SelectOption(
                label="Стрелец",
            ),
            discord.SelectOption(
                label="Козерог",
            ),
            discord.SelectOption(
                label="Водолей",
            ),
            discord.SelectOption(
                label="Рыбы",
            )
        ]
    )
    async def select_callback(self, interaction, select): # the function called when the user is done selecting options
        zodiac_dict = {
            'Овен': 'aries',
            'Телец': 'taurus',
            'Близнецы': 'gemini',
            'Рак': 'cancer',
            'Лев': 'leo',
            'Дева': 'virgo',
            'Весы': 'libra',
            'Скорпион': 'scorpio',
            'Стрелец': 'sagittarius',
            'Козерог': 'capricorn',
            'Водолей': 'aquarius',
            'Рыбы': 'pisces',
        }
        self.zodiac_sign = zodiac_dict[select.values[0]]
        self.stop()
        await interaction.response.send_message(f'Гороскоп на сегодня для знака {select.values[0]}:')
        await interaction.message.delete()