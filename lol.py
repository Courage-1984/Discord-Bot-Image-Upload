import discord
import os
import asyncio
import json

LOG_FILE_PATH = 'uploaded_files_log_gallery_name.json'

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
    files.sort(key=lambda x: (get_file_mtime(x[0]), x[1]))

    uploaded_files_log = load_uploaded_files_log()

    for relative_path, file_name in files:
        file_path = os.path.join(FOLDER_PATH, relative_path)

        # Use case-insensitive comparison with full path
        if os.path.normcase(os.path.abspath(file_path)) in uploaded_files_log:
            print(f"Skipping file '{file_name}' as it already exists in the channel.")
            continue

        file_size = os.path.getsize(file_path)
        if file_size > 26210390:  # Discord's limit for regular users
            print(f"Skipping file '{file_name}' as it exceeds Discord's maximum file size limit.")
            continue

        with open(file_path, 'rb') as f:
            await channel.send(file=discord.File(f, filename=file_name))

        uploaded_files_log.add(os.path.normcase(os.path.abspath(file_path)))

        # Append the uploaded file to the log file
        save_uploaded_files_log(uploaded_files_log)

        await asyncio.sleep(1.8)  # Adjust delay if needed

def load_uploaded_files_log():
    try:
        with open(LOG_FILE_PATH, 'r') as log_file:
            return set(json.load(log_file))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_uploaded_files_log(log_data):
    with open(LOG_FILE_PATH, 'w') as log_file:
        json.dump(list(log_data), log_file)

def get_file_mtime(file_path):
    try:
        return os.path.getmtime(file_path)
    except FileNotFoundError:
        return float('inf')  # Placeholder value for files with invalid paths

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    channel = client.get_channel(CHANNEL_ID)

    files_to_send = []

    for root_folder, subfolders, filenames in os.walk(FOLDER_PATH):
        relative_path = os.path.relpath(root_folder, FOLDER_PATH)
        files_with_relative_path = [(os.path.join(relative_path, filename), filename) for filename in filenames]
        files_to_send.extend(files_with_relative_path)

    await send_files_in_chronological_order(channel, files_to_send)

    await client.close()

client.run(TOKEN)
