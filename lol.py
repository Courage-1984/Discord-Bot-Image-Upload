import discord
import os
import asyncio

# Your Discord bot token
TOKEN = 'bot_token_here'

# Your server ID and channel ID
SERVER_ID = 'server_id_here'
CHANNEL_ID = channel_id_here

# Path to your folder with videos and images
FOLDER_PATH = 'folder_path_to_files_here'

# Define your intents
intents = discord.Intents.all()

client = discord.Client(intents=intents)

async def send_files_in_chronological_order(channel, files):
    # Sort files based on a custom sorting function
    files.sort(key=lambda x: (get_file_mtime(x[0]), x[1]))

    for relative_path, file_name in files:
        file_path = os.path.join(FOLDER_PATH, relative_path)
        with open(file_path, 'rb') as f:
            await channel.send(file=discord.File(f))
        await asyncio.sleep(3)  # Adjust delay if needed

def get_file_mtime(file_path):
    try:
        return os.path.getmtime(file_path)
    except FileNotFoundError:
        return float('inf')  # Placeholder value for files with invalid paths

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    server = discord.utils.get(client.guilds, id=SERVER_ID)
    channel = client.get_channel(CHANNEL_ID)

    files_to_send = []

    for root_folder, subfolders, filenames in os.walk(FOLDER_PATH):
        relative_path = os.path.relpath(root_folder, FOLDER_PATH)
        files_with_relative_path = [(os.path.join(relative_path, filename), filename) for filename in filenames]
        files_to_send.extend(files_with_relative_path)

    await send_files_in_chronological_order(channel, files_to_send)

    await client.close()

client.run(TOKEN)
