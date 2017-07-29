#!/usr/bin/env python

from morseapi import MorseRobot

import logging
import sys

from robots.concurrency import action
from robots.concurrency.signals import ActionCancelled
from robots.resources import lock, Resource


OBSTACLE_DISTANCE = 10 
NOMINAL_SPEED = 100
AVOIDANCE = Resource() 

def avoid(robot, direction):
    robot.stop()
    robot.move(-50)
    turn = 90
    if direction == "right":
        turn = -turn
    robot.turn(turn, 360/10)
    robot.drive(NOMINAL_SPEED)
    robot.cancel_all_others()

@action
@lock(AVOIDANCE)
def avoid_right(robot):
    avoid(robot, "right")

@action
@lock(AVOIDANCE)
def avoid_left(robot):
    avoid(robot, "left")

@action
@lock(AVOIDANCE)
def stop(robot):
    robot.stop()
    robot.sleep(1)
    robot.cancel_all_others()

@action
def start(robot):
    robot.drive(NOMINAL_SPEED)

@action
def left_indicator_on(robot):
    robot.left_ear_color("red")

@action
def left_indicator_off(robot):
    robot.left_ear_color("black")

@action
def right_indicator_on(robot):
    robot.right_ear_color("red")

@action
def right_indicator_off(robot):
    robot.right_ear_color("black")

def run(bot_address):
    with MorseRobot(bot_address) as robot:
        robot.connect()
        robot.reset()
        # robot.debug()
        # It would be nice to get bump sensing to work for additional obsticle avoidance.
        robot.whenever("prox_left", above=OBSTACLE_DISTANCE, max_firing_freq=5).do(avoid_left)
        robot.whenever("prox_right", above=OBSTACLE_DISTANCE, max_firing_freq=5).do(avoid_right)
        robot.whenever("picked_up", value=True, max_firing_freq=1).do(stop)
        robot.whenever("nominal", value=True, max_firing_freq=1).do(start)
        robot.whenever("dot_left_of_dash", value=True, max_firing_freq=.5).do(left_indicator_on)
        robot.whenever("dot_left_of_dash", value=False, max_firing_freq=.5).do(left_indicator_off)
        robot.whenever("dot_right_of_dash", value=True, max_firing_freq=.5).do(right_indicator_on)
        robot.whenever("dot_right_of_dash", value=False, max_firing_freq=.5).do(right_indicator_off)
        try:
            robot.drive(NOMINAL_SPEED)
            while True:
                robot.sleep(0.5)
        except KeyboardInterrupt:
            robot.stop()
            pass

if __name__ == "__main__":
    import logging
    #logging.getLogger().setLevel(logging.debug)
    bot_address = sys.argv[1] if len(sys.argv) > 1 else None 
    run(bot_address)
