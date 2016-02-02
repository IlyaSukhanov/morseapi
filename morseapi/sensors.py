import logging
import time

from morseapi.constants import CHARACTERISTICS

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

        # Accelerometer / gyro data, what fields mean is not yet clear
        self.sensor_state["ag0"] = value[2]
        self.sensor_state["ag1"] = value[3]
        self.sensor_state["ag2"] = value[4]
        self.sensor_state["ag3"] = value[5]
        self.sensor_state["ag4"] = value[6]

        self.sensor_state["mic_volume"] = value[7]

        self.sensor_state["button0"] = value[8] & 0x10 > 0
        self.sensor_state["button1"] = value[8] & 0x20 > 0
        self.sensor_state["button2"] = value[8] & 0x40 > 0
        self.sensor_state["button3"] = value[8] & 0x80 > 0

        # Unknown sensor fields
        if "unknown_dot" not in self.sensor_state:
            self.sensor_state["unknown_dot"] = {}
        self.sensor_state["unknown_dot"]["0"] = value[0] & 0x0f
        self.sensor_state["unknown_dot"]["1"] = value[1]  # always 0?
        self.sensor_state["unknown_dot"]["7"] = value[7]  # microphone volume
        self.sensor_state["unknown_dot"]["8"] = value[8] & 0x0f # awlays 0?
        self.sensor_state["unknown_dot"]["9"] = value[9]
        self.sensor_state["unknown_dot"]["10"] = value[10]
        self.sensor_state["unknown_dot"]["11"] = value[11]
        self.sensor_state["unknown_dot"]["12"] = value[12]
        self.sensor_state["unknown_dot"]["13"] = value[13]
        self.sensor_state["unknown_dot"]["14"] = value[14]
        self.sensor_state["unknown_dot"]["15"] = value[15]
        self.sensor_state["unknown_dot"]["16"] = value[16]
        self.sensor_state["unknown_dot"]["17"] = value[17]
        self.sensor_state["unknown_dot"]["18"] = value[18]
        self.sensor_state["unknown_dot"]["19"] = value[19]

        # logging.debug("self.sensor_state: {}".format(self.sensor_state))


    def _dash_sensor_decode(self, handle, value):
        self.dash_data_stream_ready = True
        self.sensor_state["dash_time"] = time.time()
        self.sensor_state["dash_index"] = value[0] >> 4
        self.sensor_state["prox_right"] = value[6]
        self.sensor_state["prox_left"] = value[7]
        self.sensor_state["prox_rear"] = value[8]
        self.sensor_state["robot_yaw"] = (value[13] << 8) | value[12]
        self.sensor_state["left_wheel"] = (value[15] << 8) | value[14]
        self.sensor_state["right_wheel"] = (value[17] << 8) | value[16]
        self.sensor_state["head_pitch"] = value[18]
        self.sensor_state["head_yaw"] = value[19]

        # Unknown sensor fields
        # missing fields: dot tracking, microphone direction
        if "unknown_dash" not in self.sensor_state:
            self.sensor_state["unknown_dash"] = {}
        self.sensor_state["unknown_dash"]["0"] = value[0] & 0x0f
        self.sensor_state["unknown_dash"]["1"] = value[1]
        self.sensor_state["unknown_dash"]["2"] = value[2]
        self.sensor_state["unknown_dash"]["3"] = value[3]
        self.sensor_state["unknown_dash"]["4"] = value[4]
        self.sensor_state["unknown_dash"]["5"] = value[5]
        self.sensor_state["unknown_dash"]["9"] = value[9]  # Changes with wheel rotation
        self.sensor_state["unknown_dash"]["10"] = value[10]  # Changes with wheel rotation
        self.sensor_state["unknown_dash"]["11"] = value[11]  # Changes with wheel rotation

        #logging.debug("self.sensor_state: {}".format(self.sensor_state))
