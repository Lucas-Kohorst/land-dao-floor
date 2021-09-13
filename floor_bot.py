import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv
import requests

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
VAULT_REFRESH_TIMER = os.getenv('REFRESH_TIMER')

client = discord.Client()

def get_floor_price():
    r = requests.get("https://api.opensea.io/api/v1/collections?asset_owner=0xFb2CE50C4c8024E037e6be52dd658E2Be23d93Db&offset=0&limit=300")
    floor_price = r.json()[0]['stats']['floor_price']
    floorstring = (f"${floor_price}ETH")
    return floorstring

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    refresh_floor_price.start()

@tasks.loop(seconds=float(VAULT_REFRESH_TIMER))
async def refresh_floor_price():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=get_floor_price()))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$floor'):
        floor = get_floor_price()
        await message.channel.send(floor)
        
client.run(TOKEN)
