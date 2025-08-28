import os
import discord
from dotenv import load_dotenv
import daily_report
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

"""
Daily weather report Discord Bot for FAU Boca Campus
"""

#Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_KEY')
CHANNEL_ID = 1410708136209289296

# Client setup
intents = discord.Intents.default()
bot = discord.Client(intents=intents)

@bot.event # Log when the bot is ready
async def on_ready():
    print(f"Logged in as {bot.user}")

    scheduler = AsyncIOScheduler()
    trigger = CronTrigger(hour=6, minute=30)

    scheduler.add_job(send_daily_report, trigger)
    scheduler.start()
    print("Daily report scheduler started.")

async def send_daily_report(): # Send the daily report to the specified channel
    try:
        channel = await bot.fetch_channel(CHANNEL_ID)
        report = daily_report.make_report()
        await channel.send(report)
        print("Daily report sent!")
    except Exception as e:
        print(f"Failed to send report: {e}")

bot.run(TOKEN)
