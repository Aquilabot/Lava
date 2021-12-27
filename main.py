#initialize a discord bot
import nextcord
import lavalink
from nextcord.activity import Spotify
from antiscam import AntiScam
from nextcord.ext import commands
from youtube_dl import YoutubeDL
from spotipy.oauth2 import SpotifyClientCredentials
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
import asyncio

#add a prefix to the bot
bot = commands.Bot(command_prefix='>')

#set start time for the bot
start_time = datetime.datetime.now()

#make a list of all the servers the bot is in
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=nextcord.Game(name='>help'))


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

#search for a song
@bot.command()
async def search(ctx, *, query):
    results = await bot.search(query)
    await ctx.send(f'{results}')

#play a song using youtube-dl
@bot.command()
async def play(ctx, *, query):
    #join the voice channel
    voice = nextcord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(ctx.author.voice.channel)
    else:
        voice = await ctx.author.voice.channel.connect()
    #determine link type
    if 'youtube.com' in query:
        url = query
    elif 'soundcloud.com' in query:
        url = query
    elif 'youtu.be' in query:
        url = query
    elif 'www.youtube.com' in query:
        url = query
    elif 'www.soundcloud.com' in query:
        url = query
    else:
        url = 'ytsearch:' + query
    #play the song if youtube or soundcloud
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            ydl.download([info['webpage_url']])
            filename = info['id'] + '.mp3'
            await ctx.send(f'Playing {info["title"]}')
            ctx.voice_client.play(nextcord.FFmpegPCMAudio(filename), after=lambda e: print('done', e))
            ctx.voice_client.source = nextcord.PCMVolumeTransformer(ctx.voice_client.source)
            ctx.voice_client.source.volume = 0.07
        #if failed to play
        if ctx.voice_client.is_playing():
            await ctx.send('Failed to play')
    #play the song spotify
    if 'open.spotify.com' in query:
        url = query
        #use spotify.json to get the client id and secret
        with open('.password-store/spotify.json') as f:
            data = json.load(f)
        #get the client id and secret
        spotify_client_id = data['client_id']
        spotify_client_secret = data['client_secret']
        #get the access token
        token = await nextcord.Spotify.get_access_token(spotify_client_id, spotify_client_secret)
        client_credentials_manager = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
        sp = Spotify.Spotify(client_credentials_manager=client_credentials_manager)
        results = sp.search(q=query, type='track')
        items = results['tracks']['items']
        for i in items:
            if i['name'] == query:
                uri = i['uri']
                await ctx.send(f'Playing {i["name"]}')
                ctx.voice_client.play(nextcord.Spotify(uri=uri), after=lambda e: print('done', e))
                ctx.voice_client.source = nextcord.PCMVolumeTransformer(ctx.voice_client.source)
                ctx.voice_client.source.volume = 0.07
        #if failed to play
        if ctx.voice_client.is_playing():
            await ctx.send('Failed to play')

#play a song using lavaplayer and the spotify api
#TODO: make this work


#stop the bot
@bot.command()
async def stop(ctx):
    await ctx.send('Stopping...')
    await bot.disconnect()

#run the bot with the token given with discord.json
#get the token with discord.json
with open('.password-store/discord.json') as f:
    data = json.load(f)
token = data['discord_token']
bot.run(token)