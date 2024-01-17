import discord
import os
import random
import asyncio

# Your Discord bot token
TOKEN = 'your_bot_token_here'

# Your server ID and channel ID
SERVER_ID = 'your_server_id_here'
CHANNEL_ID = your_channel_id_here

# Path to your folder with 900 videos and images
FOLDER_PATH = 'path_to_your_folder_here'

# Define your intents
intents = discord.Intents.all()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    server = discord.utils.get(client.guilds, id=SERVER_ID)
    # channel = discord.utils.get(server.channels, id=CHANNEL_ID)
    channel = client.get_channel(CHANNEL_ID)

    files = os.listdir(FOLDER_PATH)
    random.shuffle(files)

    for i in range(0, len(files), 10):
        batch = files[i:i+10]
        for file in batch:
            file_path = os.path.join(FOLDER_PATH, file)
            with open(file_path, 'rb') as f:
                await channel.send(file=discord.File(f))
            await asyncio.sleep(3)  # Adjust delay if needed

    await client.logout()

client.run(TOKEN)
