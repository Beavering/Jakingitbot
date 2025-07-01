import os
import threading
from flask import Flask
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
# Replace this with the User ID you want to track
TARGET_USER_ID = 735115327226249247 # Right-click the user > Copy ID (you need Developer Mode on)

intents = discord.Intents.default()
intents.presences = True
intents.members = True
role_id = 1253120317308801085

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_web).start()


bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is logged in as {bot.user}")

@bot.event
async def on_presence_update(before, after):
    if after.id == TARGET_USER_ID:
        if before.status != after.status and after.status == discord.Status.online:
            # Choose the channel by name or ID where message should go
            for guild in bot.guilds:
                for channel in guild.text_channels:
                    if channel.name == "general":  # Or replace with your channel name
                        await channel.send(f" <@&{role_id}> stop jaking it <a:jakingit:1389456598077931650> ")
                        return

# Replace YOUR_BOT_TOKEN with your actual token
bot.run(os.getenv("DISCORD_TOKEN"))