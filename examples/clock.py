#!/usr/bin/env python

import time
import pexpect
import datetime
import sys
from morseapi import MorseRobot

AMPM_COLORS = {"am": "green", "pm": "darkorange"}

def draw_now(bot):
    now = datetime.datetime.now()
    return draw_time(bot, now.hour, now.minute)

def draw_time(bot, hour, minute, blink_duration__seconds=1):
    ampm = "am" if hour < 12 else "pm"
    hour_bit = hour % 12
    minute_bit = minute * 12 / 60
    refresh_interval = blink_duration__seconds / 2.0

    hour_value = (1 << hour_bit)
    minute_value = (1 << minute_bit)

    bot.neck_color(AMPM_COLORS[ampm])
    bot.eye(hour_value)
    time.sleep(refresh_interval)
    bot.eye(hour_value | minute_value)
    time.sleep(refresh_interval)

def run(bot_address):
    print("Connecting to {0}.".format(bot_address))
    bot = MorseRobot(bot_address)
    bot.connect()
    print("Connected")
    bot.sense.stop()
    while True:
        draw_now(bot)

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    bot_address = sys.argv[1] if len(sys.argv) > 1 else None 
    run(bot_address)
