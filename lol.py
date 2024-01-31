import discord
import os
import asyncio
import hashlib

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = 'YOUR_BOT_TOKEN'

# Replace 'SERVER_ID' and 'CHANNEL_ID' with your server and channel IDs
SERVER_ID = 'SERVER_ID'  # Replace with your server ID
CHANNEL_ID = CHANNEL_ID  # Replace with your channel ID

# Path to your folder with the files in it (videos and images, etc.)
FOLDER_PATH = 'C:/path/to/folder/containing/files'

# Define your intents
intents = discord.Intents.all()

client = discord.Client(intents=intents)

async def send_files_in_chronological_order(channel, files):
    # Sort files based on a custom sorting function
    files.sort(key=lambda x: (get_file_mtime(x[0]), x[1]))

    # Mapping for Discord-renamed file names
    renamed_file_mapping = await get_renamed_file_mapping(channel)

    for relative_path, file_name in files:
        file_path = os.path.join(FOLDER_PATH, relative_path)

        # Check if the file already exists in the channel
        existing_files = await get_existing_files(channel)

        # Get the Discord-renamed file name from the mapping
        discord_renamed_file_name = renamed_file_mapping.get(file_name, file_name)

        # Replace spaces with underscores for comparison
        discord_renamed_file_name_for_comparison = discord_renamed_file_name.replace(' ', '_')

        if discord_renamed_file_name_for_comparison in existing_files:
            print(f"Skipping file '{file_name}' as it already exists in the channel.")
            continue

        with open(file_path, 'rb') as f:
            # Use the Discord-renamed file name when sending
            await channel.send(file=discord.File(f, filename=discord_renamed_file_name))
        await asyncio.sleep(3)  # Adjust delay if needed

async def get_existing_files(channel):
    existing_files = set()
    async for message in channel.history(limit=None):  # None means no limit
        for attachment in message.attachments:
            existing_files.add(attachment.filename.replace(' ', '_'))
    return existing_files

async def get_renamed_file_mapping(channel):
    # Build a mapping of original file names to Discord-renamed file names
    renamed_file_mapping = {}
    async for message in channel.history(limit=None):  # None means no limit
        for attachment in message.attachments:
            original_file_name = os.path.basename(attachment.url)
            renamed_file_mapping[original_file_name] = attachment.filename
    return renamed_file_mapping

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
