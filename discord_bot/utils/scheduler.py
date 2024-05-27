from apscheduler.schedulers.asyncio import AsyncIOScheduler
import datetime
import pytz

def schedule_wakeup_task(bot, channel_id):
    scheduler = AsyncIOScheduler()

    async def wakeup_task():
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send("Good morning, everyone! Time to rise and shine!")

    # 5AM, adjust for desired timezone
    wakeup_time = datetime.time(5, 0) 
    vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')  
    scheduler.add_job(wakeup_task, 'cron', hour=wakeup_time.hour, minute=wakeup_time.minute, timezone=vietnam_timezone)
    scheduler.start() 
