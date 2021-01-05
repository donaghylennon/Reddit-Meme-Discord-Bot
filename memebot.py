#!/usr/bin/env python3 
import os 
import discord 
from discord.ext import commands, tasks 
import praw 

SUBREDDIT = 'dankmemes'

CHANNEL_ID = os.environ.get('MY_PRIV_CHANNEL_ID')
DISCORD_CLIENT_ID = os.environ.get('DISCORD_CLIENT_ID')
REDDIT_UNM = os.environ.get('REDDIT_UNM')
REDDIT_PWD = os.environ.get('REDDIT_PWD')
REDDIT_CLIENT_ID = os.environ.get('REDDIT_CID')
REDDIT_CLIENT_SECRET = os.environ.get('REDDIT_CSEC')
REDDIT_USER_AGENT = os.environ.get('REDDIT_USER_AGENT')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')

#     await send_message()


# @tasks.loop(minutes=1)
# async def once_per_minute():
#     channel = client.get_channel(CHANNEL_ID)
#     print(f"Got channel {channel}")
#     await channel.send("Minute message")


# @once_per_minute.before_loop
# async def before_once_per_minute():
#     await client.wait_until_ready()
#     print("Finished waiting")


@tasks.loop(hours=24)
async def send_memes():
    channel = client.get_channel(CHANNEL_ID)
    reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET,
                         username=REDDIT_UNM, password=REDDIT_PWD, user_agent=REDDIT_USER_AGENT)
    subreddit = reddit.subreddit(SUBREDDIT)
    hot_posts = subreddit.hot(limit=7)
    for submission in hot_posts:
        if not submission.stickied:
            await channel.send('\"{0.title}\" - {0.author}\n{0.url}'.format(submission))


@send_memes.before_loop
async def before_memes():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('Meme bot ready')


# async def send_message():
#     channel = client.get_channel(CHANNEL_ID)
#     await channel.send('Test message')

send_memes.start()
client.run(DISCORD_CLIENT_ID)
