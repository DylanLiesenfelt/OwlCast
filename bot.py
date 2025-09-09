import os
import discord
from dotenv import load_dotenv
import daily_report
from tomorrow_client import get_current_weather
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler

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

# Weather Code Dict
weather_codes = {
    4000: 'Drizzle',
    4200: 'Light Rain',
    4100: 'Rain',
    4201: 'Heavy Rain',
    6000: 'Freezing Drizzle',
    6200: 'Light Freezing Drizzle',
    6001: 'Freezing Rain',
    6201: 'Heavy Freezing Rain',
    7102: 'Light Ice Pellets',
    7000: 'Ice Pellets',
    7101: 'Heavy Ice Pellets'
}

"""
Triggered when the bot is ready. Sets up the daily report and weather check schedulers.
"""
@bot.event 
async def on_ready():
    print(f"Logged in as {bot.user}")
    # Daily Report
    scheduler = AsyncIOScheduler()
    trigger = CronTrigger(hour=6, minute=30)
    scheduler.add_job(send_daily_report, trigger)
    print("Daily report scheduler started.")
    scheduler.start()

    bg_sched = BackgroundScheduler()
    bg_sched.add_job(check_weather, 'interval', minutes=10)

"""
Send the daily weather report at 6:30 AM every day
"""
async def send_daily_report(): 
    try:
        channel = await bot.fetch_channel(CHANNEL_ID)
        report = daily_report.make_report()
        await channel.send(report)
        print("Daily report sent!")
    except Exception as e:
        print(f"Failed to send report: {e}")


"""
Check the weather every 10 minutes and send a notification if rain is expected
"""
async def check_weather(): 
    try:
        channel = await bot.fetch_channel(CHANNEL_ID)
        if channel:
            status = get_current_weather()
            if status in weather_codes:
                weather = weather_codes[status]
                notification = f'WEATHER: {weather}'
                await channel.send(notification)
                print("Rain Notification Sent!")
    except Exception as e:
        print(f"Failed to send report: {e}")

bot.run(TOKEN)
