import os
import discord
from dotenv import load_dotenv
import daily_report
from tomorrow_client import get_current_weather
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

"""
Daily weather report Discord Bot for FAU Boca Campus
"""

# Load environment variables
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

last_weather = None

"""
Triggered when the bot is ready. Sets up the daily report and weather check schedulers.
"""
@bot.event 
async def on_ready():
    print(f"Logged in as {bot.user}")

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_report, CronTrigger(hour=6, minute=30))
    scheduler.add_job(check_weather, 'interval', minutes=4)
    scheduler.start()
    print("Schedulers started.")
    
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
        print(f"Daily report failed: {e}")


"""
Check the weather every 15 minutes and send a notification if rainy weather is expected
"""
async def check_weather(): 
    global last_weather
    print('Weather check running...')
    try:
        channel = await bot.fetch_channel(CHANNEL_ID)
        if channel:
            weather_code = get_current_weather()
            
            print('Weather Code:',weather_code)

            if weather_code is None:
                print("Weather check failed – Tomorrow.io API error.")
                return

            if weather_code != last_weather:
                if weather_code in weather_codes:
                    last_weather = weather_code
                    notification = f'Incoming Weather: {weather_code}'
                    await channel.send(notification)
                    print("Weather Notification Sent!")

            else:
                print("no change in weather status")

    except Exception as e:
        print(f"Weather check failed: {e}")

bot.run(TOKEN)
