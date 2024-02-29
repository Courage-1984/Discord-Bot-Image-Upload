import discord
from discord.ext import commands
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
bot = commands.Bot(command_prefix="!", intents=intents)

# Variable to track whether all files have been sent
all_files_sent = False

async def send_files_in_chronological_order(channel, files):
    global all_files_sent
    files.sort(key=lambda x: (get_file_mtime(os.path.join(FOLDER_PATH, x[0])), x[1]))
    uploaded_files_log = load_uploaded_files_log()

    for relative_path, file_name in files:
        if all_files_sent:
            break  # Break the loop if all files have been sent

        if os.path.normcase(file_name) in uploaded_files_log:
            print(f"Skipping file '{file_name}' as it already exists in the channel.")
            continue

        file_path = os.path.join(FOLDER_PATH, relative_path)
        file_size = os.path.getsize(file_path)

        if file_size > 26210390:
            print(f"Skipping file '{file_name}' as it exceeds Discord's maximum file size limit.")
            continue

        try:
            with open(file_path, 'rb') as f:
                await channel.send(file=discord.File(f, filename=file_name))
        except (discord.HTTPException, asyncio.TimeoutError) as e:
            if isinstance(e, discord.HTTPException):
                if "429" in str(e):  # Check if it's a rate limit error
                    print("Rate limited. Waiting for a while...")
                    await asyncio.sleep(60)  # Wait for a minute and retry
                    continue
                else:
                    print(f"Error sending file '{file_name}': {e}")
            elif isinstance(e, asyncio.TimeoutError):
                print(f"TimeoutError sending file '{file_name}': {e}")

            print("Continuing with the next file.")
            continue

        uploaded_files_log.add(os.path.normcase(file_name))
        save_uploaded_files_log(uploaded_files_log)

        print(f"File '{file_name}' sent successfully.")
        await asyncio.sleep(4)  # Adjust delay if needed

    all_files_sent = True  # Set the variable to True when all files are sent



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

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check if the message starts with the command prefix and the command is "send_files"
    if message.content.startswith('!send_files') and message.guild:
        channel = message.channel
        files_to_send = []

        for root_folder, subfolders, filenames in os.walk(FOLDER_PATH):
            relative_path = os.path.relpath(root_folder, FOLDER_PATH)
            files_with_relative_path = [(os.path.join(relative_path, filename), filename) for filename in filenames]
            files_to_send.extend(files_with_relative_path)

        await send_files_in_chronological_order(channel, files_to_send)

    await bot.process_commands(message)



@bot.command()
async def send_files(ctx):
    channel = ctx.channel
    files_to_send = []

    for root_folder, subfolders, filenames in os.walk(FOLDER_PATH):
        relative_path = os.path.relpath(root_folder, FOLDER_PATH)
        files_with_relative_path = [(os.path.join(relative_path, filename), filename) for filename in filenames]
        files_to_send.extend(files_with_relative_path)

    await send_files_in_chronological_order(channel, files_to_send)

    # Stop the bot after sending all files
    await bot.close()

bot.run(TOKEN)
