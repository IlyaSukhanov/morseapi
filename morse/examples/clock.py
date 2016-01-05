import time
import pexpect
import datetime
from ..control  import WonderControl

DOT = "C0:F0:84:3C:51:FA"

def draw_now(bot):
    now = datetime.datetime.now()
    return draw_time(bot, now.hour, now.minute)

def draw_time(bot, hour, minute, duration=.25):
    hour_bit = (hour - 1) % 12
    minute_bit = minute * 12 / 60
    end_time = time.time() + duration

    hour_value = (1 << hour_bit)
    minute_value = (1 << minute_bit)

    while time.time() < end_time:
            bot.eye(hour_value)
            time.sleep(.1)
            bot.eye(hour_value | minute_value)
            time.sleep(.1)

if __name__ == "__main__":
    bot = WonderControl(DOT)
    while True:
        draw_now(bot)
