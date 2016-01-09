import pygatt.backends
import time
import logging
import struct
import binascii
import math
import sys
from colour import Color

BOTS = {
    "dash": "EB:C9:96:2D:EA:48",
    "dot": "C0:F0:84:3C:51:FA",
}
DEVICE_HANDLE = 19
COMMANDS={
    "neck_color":0x03,
    "eye_brightness":0x08,
    "eye":0x09,
    "left_ear_color":0x0b,
    "right_ear_color":0x0c,
    "head_color":0x0d,
    "head_pitch":0x07,
    "head_yaw":0x06,
    "say":0x18,
    "move":0x23,
}

NOISES={
    k:v.decode("hex")
    for (k,v) in {
        "elephant":   "53595354454c455048414e545f300e460000",  # SYSTELEPHANT_0.F
        "tiresqueal": "535953545449524553515545414c0e460000",  # SYSTTIRESQUEAL.F
        "hi":         "53595354444153485f48495f564f0b00c900",  # SYSTDASH_HI_VO
        "bragging":   "535953544252414747494e4731410b232300",  # SYSTBRAGGING1A##
        "ohno":       "5359535456375f4f484e4f5f30390b000000",  # SYSTV7_OHNO_09
        "ayayay":     "53595354434f4e46555345445f310b000000",  # SYSTCONFUSED_1
        "confused2":  "53595354434f4e46555345445f320b000000",  # SYSTCONFUSED_2
        "confused3":  "53595354434f4e46555345445f330b000000",  # SYSTCONFUSED_3
        "confused5":  "53595354434f4e46555345445f350b000000",  # SYSTCONFUSED_5
        "confused8":  "53595354434f4e46555345445f380b000000",  # SYSTCONFUSED_8
        "brrp":       "53595354434f4e46555345445f360b000000",  # SYSTCONFUSED_6
        "charge":     "535953544348415247455f3033000b000000",  # SYSTCHARGE_03
    }.items()}

def one_byte_array(value):
    return bytearray(struct.pack(">B", value))

def two_byte_array(value):
    return bytearray(struct.pack(">H", value))

def color_byte_array(color_value):
    color = Color(color_value)
    return bytearray([
        int(color.get_red()*255),
        int(color.get_green()*255),
        int(color.get_blue()*255),
    ])

def angle_array(angle):
    if angle < 0:
        angle = (abs(angle) ^ 0xff) + 1
    return bytearray([angle & 0xff])

class WonderControl(object):
    def __init__(self, address=None):
        self.address = address

    def _connect(self):
        if self.address:
            adapter = pygatt.backends.GATTToolBackend()
            adapter.start()
            self.device = adapter.connect(address, address_type='random')

    def command(self, command_name, command_values):
        message = bytearray([COMMANDS[command_name]]) + command_values
        logging.debug(binascii.hexlify(message))
        if self.address:
            self.device.char_write_handle(DEVICE_HANDLE, message)

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

    def turn(self, degrees):
        """
        Turn robot degrees to left. Negative degrees to turn right.
        """
        if abs(degrees)>360:
            raise NotImplementedError("Cannot turn more than one rotation per move")
        if degrees:
            byte_array = self._get_move_byte_array(degrees=degrees, seconds=degrees*(2.094/360.0))
            self.command("move", byte_array)

    def move(self, distance_millimetres, speed_mmps=1000.0):
        seconds = distance_millimetres / speed_mmps
        byte_array = self._get_move_byte_array(distance_millimetres=distance_millimetres, seconds=seconds)
        self.command("move", byte_array)

    def _get_move_byte_array(self, distance_millimetres=0, degrees=0, seconds=1.0):
        if distance_millimetres and degrees:
            # Sixth byte is mixed use
            # * turning
            #   * high nibble is turn distance high byte<<2
            #   * low nibble is 0
            # * driving straight
            #   * whole byte is high byte of drive distance
            # unclear if these can be combined
            raise NotImplementedError("Cannot turn and drive concurrently")

        seventh_byte = 0

        distance_low_byte = distance_millimetres & 0x00ff
        distance_high_byte = (distance_millimetres & 0xff00) >> 8
        sixth_byte = distance_high_byte

        centiradians = int(math.radians(degrees) * 100.0)
        turn_low_byte = centiradians & 0x00ff
        turn_high_byte = (centiradians & 0x0300) >> 2
        sixth_byte = turn_high_byte
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
    bot = WonderControl(bot_name)
    for i in range(0, 9):
        bot.turn(45*i)
    for i in range(0, 9):
        bot.turn(-45*i)
