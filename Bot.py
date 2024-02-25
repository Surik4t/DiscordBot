import os
import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from MyOpenAiModule import GPT
from SaveLogs import FileEdit

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
#intents.voice_states = True  

bot = commands.Bot(command_prefix = '!', intents = intents)

@bot.command(name = 'artitest')
async def test(ctx):
    response = "Да-да, я живой"
    await ctx.send(response)

@bot.command(name = 'artihelp')
async def artihelp(ctx):
    response = '''
**!gpt** пообщайтесь с chat-gtp! Артибот использует модель gpt-3.5-turbo.
**!gpt clear_context** очищает контекст последних сообщений чата gpt'''

    await ctx.reply(response)

Gpt = GPT()
f = FileEdit()

@bot.command(name = 'gpt')
async def gpt(ctx, *, message: str):

    channel_name = ctx.channel.name
    filename = channel_name + '.txt'

    if message == 'clear_context':
        f.clear_context(filename)
        await ctx.send('GPT контекст сброшен')
        return()

    username = ctx.author.display_name
    f.write_to_file(filename, username, message)

    message = f.get_context(filename)
    print (message)

    response = Gpt.send_prompt(message) 
    f.write_to_file(filename, 'assistant', response)
    print("assistant: " + response)

    await ctx.reply(response) 


        
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Недостаточно прав')

@bot.event 
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@bot.event
async def on_voice_state_update(member, before, after):
    nick = member.display_name
    current_ch = after.channel
    last_ch = before.channel
    guild = member.guild
    create_vc = get(guild.voice_channels, name = 'Создать')
    
    #Check if we just connected to a channel
    if current_ch != None:
        if last_ch == None:
#   if current_ch.category == create_vc.category:
            if current_ch == create_vc:
                new_channel = await voice_channel_create(current_ch, nick, member)
                await member.move_to(new_channel)
        else:
            if last_ch != create_vc and last_ch.category == create_vc.category:
                if len(last_ch.members) == 0:
                    await last_ch.delete()
            if current_ch == create_vc:
                new_channel = await voice_channel_create(current_ch, nick, member)
                await member.move_to(new_channel)     
    #Check if we left our channel, delete channel if empty 
    else:
        if last_ch.category == create_vc.category:
            if last_ch != create_vc and last_ch.category == create_vc.category:
                if len(last_ch.members) == 0:
                    await last_ch.delete()
                    
                  
async def voice_channel_create(channel, ch_name, member):
    new_channel = await channel.guild.create_voice_channel(name = ch_name,
                                                   category = channel.category,
                                                   user_limit = 5)
    await new_channel.set_permissions(member,
                              manage_channels = True,
                              mute_members = True,
                              move_members = True,
                              manage_permissions = True,
                              create_instant_invite = True)
    return(new_channel)

bot.run(TOKEN)





'''
@bot.command(name = 'create_vc')
async def create_channel(ctx, arg = None):
    author = ctx.author
    guild = ctx.guild
    channel_name = ctx.author.display_name
    existing_channel = discord.utils.get(guild.channels, id = author.id)
    channel_category = discord.utils.get(guild.categories, name = 'Голосовые каналы')

    if not existing_channel:
        response = 'Создаю голосовой канал: ' + channel_name    

        # Creating channel without limits by default
        if arg is None:
            await ctx.reply(response)
            await guild.create_voice_channel(name = channel_name, category = channel_category)  
        # Creating limited channel   
        else:
            try:
                arg = int(arg)
                if arg > 99: arg = 99
                if arg < 0: arg = 0
                await ctx.reply(response)
                await guild.create_voice_channel(name = channel_name, category = channel_category, user_limit = int(arg))
        # Parameter error        
            except ValueError:
                response = 'Параметр должен быть целым числом'
                await ctx.reply(response)

        channel = get(guild.voice_channels, name = channel_name)
        await channel.set_permissions(author,
                                      manage_channels = True,
                                      mute_members = True,
                                      move_members = True,
                                      manage_permissions = True)
        channel.id = author.id 

        # Abort if channel already exists    
    else:
        channel = get(guild.voice_channels, id = author.id).name

        response = 'У тебя уже есть канал: ' + channel
        await ctx.reply(response)
'''























