import unittest
from collections import defaultdict
from mock import MagicMock, patch

from morseapi import MorseSense
from morseapi import NOISES


DASH_RAW_SENSOR = bytearray(
    "809600ffffff0101ff0f34ed9ce1fce55c190405"
    .decode("hex")
)
DASH_DECODED_SENSOR = {
    'acceleration': 956,
    'dash_index': 8,
    'head_pitch': 4,
    'head_yaw': 5,
    'prox_left': 1,
    'prox_rear': 255,
    'prox_right': 1,
    'right_wheel': 6492,
    'roll_delta': -1,
    'wheel_distance': -716,
    'yaw': 53660,
    'yaw_delta': 53660,
}
DOT_RAW_SENSOR = bytearray(
    "8000d227f030bc0000000030ff35e30800000000"
    .decode("hex")
)
DOT_DECODED_SENSOR = {
    'button0': False,
    'button1': False,
    'button2': False,
    'button3': False,
    'clap': False,
    'dot_index': 8,
    'mic_level': 0,
    'moving': False,
    'nominal': True,
    'pitch': -46,
    'roll': 39,
    # Decoding to the rest is bit iffy
    # 'dot_left_of_dash': False,
    # 'dot_right_of_dash': False,
    # 'hit': False,
    # 'picked_up': False,
    # 'side': True,
}

class RobotTests(object):
    def setup_helper(self):
        self.conn = MagicMock()
        self.sensor_state = defaultdict(int) 
        self.sense = MorseSense(self.conn, self.sensor_state)
        self.conn.subscribe = MagicMock(
            side_effect=self.subscribe_side_effect()
        )
        self.conn.unscribe = MagicMock()
        self.sense.start(.001)

    def assert_bot_detection(self, robot):
        self.assertEqual(self.sensor_state['robot'], robot)

    def assert_sensor_data(self, decoded_sensor):
        
        for key, value in decoded_sensor.iteritems():
            self.assertEqual(self.sensor_state[key], value)

    def assert_start(self):
        self.assertEqual(self.conn.subscribe.call_count, 2)

    def assert_stop(self):
        self.assertEqual(self.conn.subscribe.call_count, 2)
        self.conn.reset_mock()
        self.sense.unsubscribe()
        self.assertEqual(self.conn.unsubscribe.call_count, 2)


class FailBotTest(RobotTests, unittest.TestCase):
    def test_no_data(self):
        with self.assertRaises(RuntimeError):
            self.setup_helper()

    def subscribe_side_effect(self):
        pass


class DotSenseTest(RobotTests, unittest.TestCase):
    def setUp(self):
        self.setup_helper()

    def subscribe_side_effect(self):
        self.sense.dot_data_stream_ready = True
        self.sense._dot_sensor_decode(None, DOT_RAW_SENSOR)

    def test_dot_detection(self):
        self.assert_bot_detection("dot")

    def test_dot_sensor_data(self):
        self.assert_sensor_data(DOT_DECODED_SENSOR)

    def test_dot_start(self):
        self.assert_start()

    def test_dot_stop(self):
        self.assert_stop()


class DashSenseTest(RobotTests, unittest.TestCase):
    def setUp(self):
        self.setup_helper()

    def subscribe_side_effect(self):
        self.sense.dash_data_stream_ready = True
        self.sense.dot_data_stream_ready = True
        self.sense._dot_sensor_decode(None, DOT_RAW_SENSOR)
        self.sense._dash_sensor_decode(None, DASH_RAW_SENSOR)

    def test_dash_detection(self):
        self.assert_bot_detection("dash")

    def test_dash_sensor_data(self):
        self.assert_sensor_data(DOT_DECODED_SENSOR)
        self.assert_sensor_data(DASH_DECODED_SENSOR)
        
    def test_dash_start(self):
        self.assert_start()

    def test_dash_stop(self):
        self.assert_stop()
