import unittest
from mock import MagicMock

from morseapi import MorseRobot
from morseapi import NOISES

class MorseRobotCommandsTest(unittest.TestCase):
    def setUp(self):
        self.bot = MorseRobot(None)
        self.bot.command = MagicMock()

    def _assert_command_called(self, command_name, command_value):
        self.bot.command.assert_called_once_with(
            command_name,
            bytearray(command_value.decode("hex"))
        )
        self.bot.command.reset_mock()

    def _move_tester(self, distance, speed, command):
        self.bot.move(distance, speed)
        self._assert_command_called("move", command)

    def test_move_1000_forward_fast(self):
        self._move_tester(1000, 600, "e800000682030040")

    def test_move_1000_backward_fast(self):
        self._move_tester(-1000, 600.0, "18000006823c0040")

    def test_move_500_backward_slow(self):
        self._move_tester(-500, 80, "0c0000186a3e0040")

    def test_turn_360_right(self):
        self.bot.turn(-360)
        self._assert_command_called("move", "00008c082e40c040")

    def test_turn_360_left(self):
        self.bot.turn(360)
        self._assert_command_called("move", "000074082e800040")

    def test_stop(self):
        self.bot.stop()
        self._assert_command_called("drive", "000000")

    def test_forward_fast(self):
        self.bot.drive(300)
        self._assert_command_called("drive", "2c0001")

    def test_backward_normal(self):
        self.bot.drive(-200)
        self._assert_command_called("drive", "380007")

    def test_spin_right(self):
        self.bot.spin(-200)
        self._assert_command_called("drive", "003838")

    def test_spin_left(self):
        self.bot.spin(200)
        self._assert_command_called("drive", "00c800")

    def test_red_neck(self):
        self.bot.neck_color("red")
        self._assert_command_called("neck_color", "ff0000")

    def test_lime_left_ear(self):
        self.bot.left_ear_color("lime")
        self._assert_command_called("left_ear_color", "00ff00")

    def test_blue_right_ear(self):
        self.bot.right_ear_color("blue")
        self._assert_command_called("right_ear_color", "0000ff")

    def test_fuchsia_head(self):
        self.bot.head_color("Fuchsia")
        self._assert_command_called("head_color", "ff00ff")

    def test_rest(self):
        self.bot.reset()
        self._assert_command_called("reset", "04")

    def test_min_yaw(self):
        self.bot.head_yaw(-53)
        self._assert_command_called("head_yaw", "cb")

    def test_max_yaw(self):
        self.bot.head_yaw(53)
        self._assert_command_called("head_yaw", "35")

    def test_min_pitch(self):
        self.bot.head_pitch(-5)
        self._assert_command_called("head_pitch", "fb")

    def test_max_pitch(self):
        self.bot.head_pitch(10)
        self._assert_command_called("head_pitch", "0a")

    def say(self):
        self.bot.say("hi")
        self._assert_command_called("say", bytearray(NOISES["hi"]))

