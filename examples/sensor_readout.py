from morseapi import MorseRobot

import logging
import sys
import os

from robots.concurrency import action
from robots.concurrency.signals import ActionCancelled
from robots.resources import lock, Resource

def run(bot_address):
    with MorseRobot(bot_address) as robot:
        robot.connect()
        robot.reset()
        try:
            while True:
                robot.sleep(.5)
                os.system('clear')
                os.system('setterm -cursor off')
                for key, value in robot.sensor_state.iteritems():
                    print("{:<20}:{:6}".format(key, value))
                os.system('setterm -cursor on')
        except KeyboardInterrupt:
            robot.stop()
            pass

if __name__ == "__main__":
    import logging
    #logging.getLogger().setLevel(logging.debug)
    bot_address = sys.argv[1] if len(sys.argv) > 1 else None
    run(bot_address)
