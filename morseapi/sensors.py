import logging
import time

from morseapi.constants import CHARACTERISTICS

def _to_int(value, bits):
    if value > ((1<<(bits-1))-1):
        return  value - (1<<bits)
    else:
        return value

class MorseSense(object):
    def __init__(self, connection, sensor_state):
        """
        Enable Robot sensors, writing results back into sensor_state dict

        :param connection: pygatt device connectio
        :param sensor_state: robot sensor_state dict
        """
        self.sensor_state = sensor_state
        self.connection = connection
        self.dot_data_stream_ready = False
        self.dash_data_stream_ready = False

    def start(self, timeout=1.0):
        """
        Subscribe to sensor notifications, but block until we've received
        enough events to determine whether its a dash or dot robot.

        Dash has two sensor streams but Dot only one. We subsribe to both
        regardless. If we get data from dash stream we then know that
        its a dash type robot.
        """
        self.subscribe()

        time.sleep(timeout)
        if self.dash_data_stream_ready and self.dot_data_stream_ready:
            self.sensor_state["robot"] = "dash"
        elif self.dot_data_stream_ready:
            self.sensor_state["robot"] = "dot"
        else:
            raise RuntimeError(
                "Failed to initialize sensor reading within {0} seconds"
                .format(timeout)
            )

    def subscribe(self):
        """
        Subscribe to sensor notification.
        """
        self.connection.subscribe(CHARACTERISTICS["dot_sensor"], self._dot_sensor_decode)
        self.connection.subscribe(CHARACTERISTICS["dash_sensor"], self._dash_sensor_decode)

    def unsubscribe(self):
        """
        Unsubsribe from sensor notification.
        """
        self.connection.unsubscribe(CHARACTERISTICS["dot_sensor"])
        self.connection.unsubscribe(CHARACTERISTICS["dash_sensor"])

    def _dot_sensor_decode(self, handle, value):
        self.dot_data_stream_ready = True
        self.sensor_state["dot_time"] = time.time()
        self.sensor_state["dot_index"] = value[0] >> 4
        #self.sensor_state["raw_dot"] = value[:]
        self.sensor_state["pitch"] = _to_int(
            (value[4] & 0xf0) << 4 | value[2],
            12
        )
        self.sensor_state["roll"] = _to_int(
            (value[4] & 0xf) << 8 | value[3],
            12
        )
        self.sensor_state["acceleration"] = _to_int(
            (value[5] & 0xf0) << 4 | value[6],
            12
        )
        self.sensor_state["button0"] = value[8] & 0x10 > 0
        self.sensor_state["button1"] = value[8] & 0x20 > 0
        self.sensor_state["button2"] = value[8] & 0x40 > 0
        self.sensor_state["button3"] = value[8] & 0x80 > 0

        # byte 11
        # 0x30 when nominal position
        # 0x24 when on side
        # 0x04 when picked up
        # 0x00 when wheels moving
        # 0x01 when bumped, last bit ONLY active bit of byte 11 on dot
        # 0x25 picked up and bumped
        self.sensor_state["moving"] = value[11] == 0
        self.sensor_state["picked_up"] = bool(value[11] & 0x04)
        self.sensor_state["hit"] = bool(value[11] & 0x01)
        self.sensor_state["side"] = value[11] & 0x20 == 0x20
        self.sensor_state["nominal"] = value[11] & 0x30 == 0x30


        self.sensor_state["clap"] = (value[11] & 1) == 1
        self.sensor_state["mic_level"] = value[7]
        if value[15] == 4:
            self.sensor_state["sound_direction"] = value[13] << 8 | value[12]

        # Dash sensing of dot; Dash only, there might be more states here
        # there are false positice reading mostly on reflective surfaces
        self.sensor_state["dot_left_of_dash"] = value[16] & 0x0f not in [0x0f, 0x0]
        self.sensor_state["dot_right_of_dash"] = value[16] & 0xf0 not in [0xf0, 0x0]
        # This seems to be another way of dash sensing dot, but its not
        # very accurate either
        # self.sensor_state["dot_left_of_dash"] = (
        #     value[19] == 5 and value[17] == 0xAA
        # )
        # self.sensor_state["dot_right_of_dash"] = (
        #     value[19] == 5 and value[18] == 0xAA
        # )

        # Unknown sensor fields
        #if "unknown_dot" not in self.sensor_state:
        #    self.sensor_state["unknown_dot"] = {}
        #self.sensor_state["unknown_dot"]["0"] = value[0] & 0x0f
        #self.sensor_state["unknown_dot"]["1"] = value[1]  # always 0?
        #self.sensor_state["unknown_dot"]["8"] = value[8] & 0x0f # awlays 0?
        #self.sensor_state["unknown_dot"]["9"] = value[9]
        #self.sensor_state["unknown_dot"]["10"] = value[10]
        #self.sensor_state["unknown_dot"]["14"] = value[14]
        # partially known:
        #self.sensor_state["unknown_dot"]["15"] = value[15]
        #self.sensor_state["unknown_dot"]["17"] = value[17]
        #self.sensor_state["unknown_dot"]["18"] = value[18]
        #self.sensor_state["unknown_dot"]["19"] = value[19]


    def _dash_sensor_decode(self, handle, value):
        self.dash_data_stream_ready = True
        self.sensor_state["dash_time"] = time.time()
        #self.sensor_state["raw_dash"] = value[:]
        self.sensor_state["dash_index"] = value[0] >> 4
        self.sensor_state["pitch_delta"] = _to_int(
            (value[4] & 0x30) << 4 | value[3],
            10
        )
        self.sensor_state["roll_delta"] = _to_int(
            (value[4] & 0x3) << 8 | value[5],
            10
        )
        self.sensor_state["prox_right"] = value[6]
        self.sensor_state["prox_left"] = value[7]
        self.sensor_state["prox_rear"] = value[8]
        yaw = _to_int((value[13]  << 8) | value[12], 12)
        self.sensor_state["yaw_delta"] = yaw  - self.sensor_state["yaw"]
        self.sensor_state["yaw"] = yaw

        self.sensor_state["left_wheel"] = (value[15] << 8) | value[14]
        self.sensor_state["right_wheel"] = (value[17] << 8) | value[16]
        self.sensor_state["head_pitch"] = value[18]
        self.sensor_state["head_yaw"] = value[19]
        self.sensor_state["wheel_distance"] = _to_int(
            (value[9] & 0xf) << 12 | value[11] << 8 | value[10],
            16
        )

        # Unknown sensor fields
        # missing fields: dot tracking, microphone direction
        #if "unknown_dash" not in self.sensor_state:
        #    self.sensor_state["unknown_dash"] = {}
        #self.sensor_state["unknown_dash"]["0"] = value[0] & 0x0f
        #self.sensor_state["unknown_dash"]["1"] = value[1]
        #self.sensor_state["unknown_dash"]["2"] = value[2]

        #logging.debug("self.sensor_state: {}".format(self.sensor_state))
