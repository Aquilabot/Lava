#initialize a discord bot
import nextcord
from nextcord.activity import Spotify
from antiscam import AntiScam
from music import Music
from music import setup
from nextcord.ext import commands
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import asyncio
import os
import random
import time
import datetime
import json
import requests
import urllib.parse
import urllib.error
import urllib.request
import urllib.error
import re
import sys
import traceback
import aiohttp

#add a prefix to the bot
bot = commands.Bot(command_prefix='<')

#set start time for the bot
start_time = datetime.datetime.now()

#make a list of all the servers the bot is in
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=nextcord.Game(name='<help'))


#make a command to ping the bot with milliseconds
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


#make a command to get the bot's uptime
@bot.command()
async def uptime(ctx):
    await ctx.send(f'Uptime: {str(datetime.timedelta(seconds=round(time.time() - start_time)))}')

#make a command to get the bot's version
@bot.command()
async def version(ctx):
    await ctx.send(f'Version: {sys.version}')

#make a command to get the bot's owner
@bot.command()
async def owner(ctx):
    await ctx.send(f'Owner: {bot.get_user(bot.owner_id)}')

#make a command to get the bot's invite link
@bot.command()
async def invite(ctx):
    await ctx.send(f'Invite: https://discordapp.com/oauth2/authorize?client_id={bot.user.id}&scope=bot%20applications.commands&permissions=8')

#create verification system
@bot.listen()
async def on_member_join(member):
    role = nextcord.utils.get(member.guild.roles, name='Verificado')
    await member.add_roles(role)

#anti-scam system
whitelist = [468499904545685507, 336924875560189954, 915984579960139816, 918520308888117259]
@bot.listen()
async def on_message(message):
    await AntiScam(message, bot = bot, whitelist = whitelist, muted_role='Muted', verified_role='Verificado') # Here you can change the names of the roles.

#setup the music cog
bot.add_cog(Music(bot))

#run the bot with the token given with discord.json
#get the token with discord.json
with open('.password-store/discord.json') as f:
    data = json.load(f)
token = data['discord_token']
bot.run(token)