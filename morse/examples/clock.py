import time
import pexpect
import datetime
from ..control  import WonderControl

DOT = "C0:F0:84:3C:51:FA"

def draw_now(bot):
    now = datetime.datetime.now()
    return draw_time(bot, now.hour, now.minute)

def draw_time(bot, hour, minute, blink_frequency=1):
    hour_bit = hour % 12
    minute_bit = minute * 12 / 60
    refresh_interval = 0.5 / blink_frequency

    hour_value = (1 << hour_bit)
    minute_value = (1 << minute_bit)

    bot.eye(hour_value)
    time.sleep(refresh_interval)
    bot.eye(hour_value | minute_value)
    time.sleep(refresh_interval)

if __name__ == "__main__":
    bot = WonderControl(DOT)
    while True:
        draw_now(bot)
