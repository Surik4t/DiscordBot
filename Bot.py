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
intents.members = True
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

gpt = GPT()
f = FileEdit()

@bot.command(name = 'gpt')
async def chat_gpt(ctx, *, message: str):

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

    response = gpt.send_prompt(message) 
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
async def on_member_join(member):
    guild = member.guild
    channel = guild.channels[0].channels[0]
    content = f'Поприветствуй нового участника {member} на сервере и поцелуй его'
    print(content)
    response = gpt.send_prompt(content)
    await channel.send(response)
    

@bot.event
async def on_voice_state_update(member, before, after):
    nick = member.display_name
    guild = member.guild
    VC_maker = get(guild.voice_channels, name = 'Создать')
    
    if after.channel == VC_maker:
        new_channel = await voice_channel_create(after.channel, nick, member)
        await member.move_to(new_channel)
        
    if before.channel == None:
        return    
    
    if before.channel.category == VC_maker.category and before.channel != VC_maker and len(before.channel.members) == 0:
        await before.channel.delete()
        
  
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




