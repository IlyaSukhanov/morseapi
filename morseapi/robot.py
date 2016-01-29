from __future__ import division
import time
import logging
import struct
import binascii
import math
import sys

from robots import GenericRobot
#from robots.decorators import action, lock
from robots.resources import Resource
#from robots.signals import ActionCancelled

from colour import Color
import pygatt.backends

from sensors import MorseSense
from constants import BOTS, HANDLES, CHARACTERISTICS, COMMANDS, NOISES

def one_byte_array(value):
    return bytearray(struct.pack(">B", value))

def two_byte_array(value):
    return bytearray(struct.pack(">H", value))

def color_byte_array(color_value):
    color = Color(color_value)
    return bytearray([
        int(round(color.get_red()*255)),
        int(round(color.get_green()*255)),
        int(round(color.get_blue()*255)),
    ])

def angle_array(angle):
    if angle < 0:
        angle = (abs(angle) ^ 0xff) + 1
    return bytearray([angle & 0xff])

#class MorseRobot(object):
class MorseRobot(GenericRobot):
    def __init__(self, address=None):
        super(MorseRobot, self).__init__()
        self.sensor_state = {}
        self.address = address
        self._connection = None

    @property
    def connection(self):
        if self._connection:
            return self._connection
        elif self.address:
            adapter = pygatt.backends.GATTToolBackend()
            adapter.start(False)
            self._connection = adapter.connect(self.address, address_type='random')
            self.sense = MorseSense(self._connection, self.sensor_state, "dash")
            return self._connection
        else:
            return None

    def command(self, command_name, command_values):
        message = bytearray([COMMANDS[command_name]]) + command_values
        logging.debug(binascii.hexlify(message))
        if self.connection:
            self.connection.char_write_handle(HANDLES["command"], message)

    def reset(self, mode=4):
        """
        Reset robot
        :param mode: Reset mode

        Available modes:
        1 some kind of debug/reflash mode?
        3 reboot
        4 zero out leds/head
        """
        self.command("reset", bytearray([mode]))
 
    def eye(self, value):
        self.command("eye", two_byte_array(value))

    def eye_brightness(self, value):
        self.command("eye_brightness", one_byte_array(value))

    def neck_color(self, color):
        self.command("neck_color", color_byte_array(color))

    def left_ear_color(self, color):
        self.command("left_ear_color", color_byte_array(color))

    def right_ear_color(self, color):
        self.command("right_ear_color", color_byte_array(color))

    def ear_color(self, color):
        self.left_ear_color(color)
        self.right_ear_color(color)

    def head_color(self, color):
        self.command("head_color", color_byte_array(color))

    def head_yaw(self, angle):
        """
        Angle range is from -53 to 53
        """
        angle = max(-53, angle)
        angle = min(53, angle)
        self.command("head_yaw", angle_array(angle))

    def head_pitch(self, angle):
        """
        Angle range is from -5 to 10
        """
        angle = max(-5, angle)
        angle = min(10, angle)
        self.command("head_pitch", angle_array(angle))

    def say(self, sound_name):
        self.command("say", bytearray(NOISES[sound_name]))

    def stop(self):
        self.command("drive", bytearray([0,0,0]))

    def drive(self, speed):
        speed = max(-2048, speed)
        speed = min(2048, speed)
        if speed < 0:
            speed = 0x800 + speed
        self.command("drive", bytearray([
            speed & 0xff,
            0x00,
            (speed & 0x0f00) >> 8
        ]))

    def spin(self, speed):
        speed = max(-2048, speed)
        speed = min(2048, speed)
        if speed < 0:
            speed = 0x800 + speed
        self.command("drive", bytearray([
            0x00,
            speed & 0xff,
            (speed & 0xff00) >> 5
        ]))

    def turn(self, degrees):
        """
        Turn robot degrees to left. Negative degrees to turn right.
        """
        if abs(degrees)>360:
            raise NotImplementedError("Cannot turn more than one rotation per move")
        if degrees:
            seconds=abs(degrees*(2.094/360))
            byte_array = self._get_move_byte_array(degrees=degrees, seconds=seconds)
            self.command("move", byte_array)
            time.sleep(seconds)
 
    def move(self, distance_millimetres, speed_mmps=1000):
        seconds = abs(distance_millimetres / speed_mmps)
        byte_array = self._get_move_byte_array(distance_millimetres=distance_millimetres, seconds=seconds)
        self.command("move", byte_array)
        time.sleep(seconds)

    def _get_move_byte_array(self, distance_millimetres=0, degrees=0, seconds=1.0):
        if distance_millimetres and degrees:
            # Sixth byte is mixed use
            # * turning
            #   * high nibble is turn distance high byte<<2
            #   * low nibble is 0
            # * driving straight
            #   * whole byte is high byte of drive distance
            # unclear if these can be combined
            raise NotImplementedError("Cannot turn and move concurrently")

        sixth_byte = 0
        seventh_byte = 0

        distance_low_byte = distance_millimetres & 0x00ff
        distance_high_byte = (distance_millimetres & 0x3f00) >> 8
        sixth_byte |= distance_high_byte

        centiradians = int(math.radians(degrees) * 100.0)
        turn_low_byte = centiradians & 0x00ff
        turn_high_byte = (centiradians & 0x0300) >> 2
        sixth_byte |= turn_high_byte
        if centiradians < 0:
            seventh_byte = 0xc0

        time_measure = int(seconds * 1000.0)
        time_low_byte = time_measure & 0x00ff
        time_high_byte = (time_measure & 0xff00) >> 8

        return bytearray([
            distance_low_byte,
            0x00,  # unknown
            turn_low_byte,
            time_high_byte,
            time_low_byte,
            sixth_byte,
            seventh_byte,
            0x40, # unknown
        ])

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    bot_name = BOTS[sys.argv[1]] if len(sys.argv)>1 else None
    bot = MorseRobot(bot_name)
    #for i in range(0, 9):
    #    bot.turn(45*i)
    #for i in range(0, 9):
    #    bot.turn(-45*i)
    #import time
    #while True:
    #    time.sleep(100)
    bot.spin(-200)
    bot.spin(200)
