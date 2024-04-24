import os, discord, base64, random, json
import SaveLogs, horoscope
#import MyOpenAiModule, YandexTranslate
from choose_zodiac_menu import zodiac_settings
from TextToImage import Text2ImageAPI
from fusion_model_settings import FusionModelStyleSettings, FusionModelRatioSettings
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
FUSION_API_TOKEN = os.getenv('FUSION_API_TOKEN')
FUSION_API_SECRET_TOKEN = os.getenv('FUSION_API_SECRET_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='artitest')
async def test(ctx):
    response = "Да-да, я живой"
    await ctx.send(response)

@bot.command(name='artihelp')
async def artihelp(ctx):
    response = '''
**!gpt** <запрос> - чат ГПТ
**!gpt clear_context** - удаление контекста ГПТ
**!tr <текст>** - перевод текста на русский язык
**!pic <запрос>** - генерация картинки
**!pic help** - доп параметры генерации
'''
    await ctx.reply(response)

@bot.command(name='gpt')
async def chat_gpt(ctx, *, message: str):
    phrase1 = [
        'Они прикрыли бесплатное использование API...',
        'Они убили нашего маленького бойкиссера!',
        'GPT больше не работает',
        "Бойкиссер умэр...",
    ]
    phrase2 = [
        'Чертов капитализм!',
        'Спи спокойно, маленький фурри ботик...',
        'R.I.P.',
        "И кто теперь будет целовать мальчиков? :'("
    ]
    random.shuffle(phrase1)
    random.shuffle(phrase2)
    await ctx.reply(f'{phrase1.pop()}\n{phrase2.pop()}')
    '''
                ОТКЛЮЧЕН БЕСПЛАТНЫЙ ДОСТУП К АПИ

    channel_name = ctx.channel.name
    filename = channel_name + '.txt'

    if message == 'clear_context':
        SaveLogs.clear_context(filename)
        await ctx.send('GPT контекст сброшен')
        return ()

    username = ctx.author.display_name
    SaveLogs.write_to_file(filename, username, message)

    message = SaveLogs.get_context(filename)
    print(message)

    response = await MyOpenAiModule.send_prompt(message)
    SaveLogs.write_to_file(filename, 'assistant', response)
    print("assistant: " + response)

    await ctx.reply(response)

@bot.event
async def on_member_join(member):
    guild = member.guild
    channel = guild.channels[0].channels[0]
    content = f'Поприветствуй нового участника {member} на сервере и поцелуй его'
    response = await MyOpenAiModule.send_prompt(content)
    await channel.send(response)
'''

@bot.command(name='test')
async def test(ctx):
    fusionAiSettingsSet('{"style": "anime"}')
    params = fusionAiSettingsGet()
    print(params)
    print(type(params))

def base64ToImage(img_data):
    with open("generated_image.jpg", "wb") as f:
        f.write(base64.decodebytes(img_data))
        print('image decoded')

def fusionAiSettingsSet(data):
    with open('fusionAiSettings.txt', 'w') as file:
        file.write(data)

def fusionAiSettingsGet():
    with open('fusionAiSettings.txt', 'r') as file:
        data = file.read()
        params = json.loads(data)
        return params

@bot.command(name='zodiac')
async def zodiac(ctx):
    view = zodiac_settings()
    await ctx.reply("Выбери знак зодиака", view=view)
    await view.wait()
    zodiac_sign = view.zodiac_sign
    text = await horoscope.get_horoscope(zodiac_sign)
    await ctx.reply(horoscope.parse(text))

@bot.command(name='pic')
async def convertTextToImage(ctx, *, message: str):
    if message.lower() == 'help':
        await ctx.reply('Пиши **!pic ratio** чтобы изменить формат, **!pic style** чтобы выбрать стиль')
        return
    if message.lower() == 'style':
        view = FusionModelStyleSettings()
        await ctx.reply(view=view)
        await view.wait()
        style = view.style
        settings = fusionAiSettingsGet()
        settings["style"] = style
        fusionAiSettingsSet(json.dumps(settings))
        return
    if message.lower() == 'ratio':
        view = FusionModelRatioSettings()
        await ctx.reply(view=view)
        await view.wait()
        height, width = view.height, view.width
        settings = fusionAiSettingsGet()
        settings["height"] = height
        settings["width"] = width
        fusionAiSettingsSet(json.dumps(settings))
        return

    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', FUSION_API_TOKEN, FUSION_API_SECRET_TOKEN)
    model_id = await api.get_model()
    settings = fusionAiSettingsGet()
    uuid = await api.generate(message, model_id, settings)
    waiting_phrases = [
        'Секундочку...',
        'Щас будет!',
        'Еще немножко...',
        'Секундочку, рисую картинку...',
        'В процессе...',
        'Еще парочка штрихов и...'
    ]
    random.shuffle(waiting_phrases)
    await ctx.reply(waiting_phrases.pop())
    images = await api.check_generation(uuid)

    base64ToImage(images[0].encode())

    with open('generated_image.jpg', 'rb') as f:
        picture = discord.File(f)
        await ctx.reply(file=picture)

@bot.command(name='tr')
async def yandex_translate(ctx, *, message: str):
    response, lang = await YandexTranslate.translate(message)
    await ctx.reply(f'*Автоопределение языка: {lang}* \n{response}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Недостаточно прав')

@bot.event
async def on_error(event, *args):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@bot.event
async def on_voice_state_update(member, before, after):
    nick = member.display_name
    guild = member.guild
    vc_maker = get(guild.voice_channels, name='Создать')

    if after.channel == vc_maker:
        new_channel = await voice_channel_create(after.channel, nick, member)
        await member.move_to(new_channel)

    if before.channel is None:
        return

    if before.channel.category == vc_maker.category and before.channel != vc_maker and len(before.channel.members) == 0:
        await before.channel.delete()

async def voice_channel_create(channel, ch_name, member):
    new_channel = await channel.guild.create_voice_channel(name=ch_name,
                                                           category=channel.category,
                                                           user_limit=5)
    await new_channel.set_permissions(member,
                                      manage_channels=True,
                                      mute_members=True,
                                      move_members=True,
                                      manage_permissions=True,
                                      create_instant_invite=True)
    return new_channel

bot.run(TOKEN)
