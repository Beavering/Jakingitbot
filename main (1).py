import os
import time
import threading
from flask import Flask
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# === Config ===
TARGET_USER_ID = 735115327226249247  # The user to track
role_id = 1253120317308801085        # The role to mention
cooldown_seconds = 1800               # Cooldown duration in seconds (5 minutes)
last_alert_time = 0                  # Tracks last message sent time

# === Flask Server for UptimeRobot Ping ===
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_web).start()

# === Discord Bot Setup ===
intents = discord.Intents.default()
intents.presences = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is logged in as {bot.user}")

@bot.event
async def on_presence_update(before, after):
    global last_alert_time

    if after.id == TARGET_USER_ID:
        if before.status != after.status and after.status == discord.Status.online:
            now = time.time()
            if now - last_alert_time >= cooldown_seconds:
                for guild in bot.guilds:
                    for channel in guild.text_channels:
                        if channel.name == "general":  # Change if needed
                            await channel.send(f"<@&{role_id}> stop jaking it <a:jakingit:1389456598077931650>")
                            last_alert_time = now
                            return

# === Run Bot ===
bot.run(os.getenv("DISCORD_TOKEN"))