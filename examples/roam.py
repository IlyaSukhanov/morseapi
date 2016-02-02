from morseapi import MorseRobot

import logging
import sys

from robots.concurrency import action
from robots.concurrency.signals import ActionCancelled

OBSTICLE_DISTANCE = 10 
NOMINAL_SPEED = 100

def avoid(robot, direction):
    robot.stop()
    robot.move(-50)
    turn = 90
    if direction == "left":
        turn = -turn
    robot.turn(turn, 360/10)
    robot.drive(NOMINAL_SPEED)
    
@action
def avoid_right(robot):
    avoid(robot, "right")

@action
def avoid_left(robot):
    avoid(robot, "left")

def run(bot_address):
    with MorseRobot(bot_address) as robot:
        robot.connect()
        # robot.debug()
        # It would be nice to get bump sensing to work for additional obsticle avoidance.
        robot.whenever("prox_left", above=OBSTICLE_DISTANCE, max_firing_freq=5).do(avoid_left)
        # One sensor often triggers right after the other .. they need to be linked somehow 
        # robot.whenever("prox_right", above=OBSTICLE_DISTANCE, max_firing_freq=1).do(avoid_right)
        try:
            robot.drive(NOMINAL_SPEED)
            while True:
                robot.sleep(0.5)
        except KeyboardInterrupt:
            robot.stop()
            pass

if __name__ == "__main__":
    import logging
    #logging.getLogger().setLevel(logging.DEBUG)
    bot_address = sys.argv[1] if len(sys.argv) > 1 else None 
    run(bot_address)
