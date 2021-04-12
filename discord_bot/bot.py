import os
import shutil
import random
import discord
import requests
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


client = discord.Client()
URL = 'https://www.reddit.com/r/dogpictures/top.json?sort=top&t=day&limit=25'
software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(software_names=software_names,
                               operating_systems=operating_systems, limit=100)
user_agent = user_agent_rotator.get_random_user_agent()
headers = {'user-agent': user_agent}


@client.event
async def on_ready():
    """Called upon starting the discord client"""
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    """Listens for new messages on the channel"""
    if message.author == client.user:
        return

    if message.content.startswith('!woof'):
        res = requests.get(URL, headers=headers)
        data = res.json()
        random_post = random.randrange(0, 24)
        content_url = data['data']['children'][random_post]['data']['url_overridden_by_dest']
        print(content_url)
        response = requests.get(content_url, stream=True)
        with open('img.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
            await message.channel.send(file=discord.File('img.png'))
            os.remove('img.png')

client.run(os.getenv('TOKEN'))
