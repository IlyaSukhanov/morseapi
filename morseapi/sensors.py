import logging
import time

from morseapi.constants import CHARACTERISTICS

class MorseSense(object):
    def __init__(self, connection, sensor_state, timeout=1.0):
        """
        Enable Robot sensors, writing results back into sensor_state dict

        Dash has two sensor streams but Dot only one. We subsribe to both
        regardless. If we get data from dash stream we then know that
        its a dash type robot.

        :param connection: pygatt device connectio
        :param sensor_state: robot sensor_state dict
        """
        self.sensor_state = sensor_state
        self.connection = connection
        self.start()
        self.dot_data_stream_ready = False
        self.dash_data_stream_ready = False

        time.sleep(timeout)
        if self.dash_data_stream_ready:
            self.sensor_state["robot"] = "dash"
        elif self.dot_data_stream_ready:
            self.sensor_state["robot"] = "dot"
        else:
            raise RuntimeError(
                "Failed to initialize sensor reading within {0} seconds"
                .format(timeout)
            )

    def start(self):
        """
        Subscribe to sensor notification.
        """
        self.connection.subscribe(CHARACTERISTICS["dot_sensor"], self._dot_sensor_decode)
        self.connection.subscribe(CHARACTERISTICS["dash_sensor"], self._dash_sensor_decode)

    def pause(self):
        """
        Pause sensor notification.
        """
        raise NotImplementedError("Oops")

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

        # logging.debug("self.sensor_state: {}".format(self.sensor_state))
        """
        Unknown sensor fields

        usensors = {}
        usensors["0"] = value[0] & 0x0f
        usensors["1"] = value[1]  # always 0?
        usensors["7"] = value[7]  # microphone volume
        usensors["8"] = value[8] & 0x0f # awlays 0?
        usensors["9"] = value[9]
        usensors["10"] = value[10]
        usensors["11"] = value[11]
        usensors["12"] = value[12]
        usensors["13"] = value[13]
        usensors["14"] = value[14]
        usensors["15"] = value[15]
        usensors["16"] = value[16]
        usensors["17"] = value[17]
        usensors["18"] = value[18]
        usensors["19"] = value[19]
        print(
            "1:{:08b}\t2:{:08b}\t3:{:08b}\t4:{:08b}\t5:{:08b}"
            .format(value[1], value[2], value[3], value[4], value[5])
        )
        """

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
        # logging.debug("self.sensor_state: {}".format(self.sensor_state))
        """
        Unknown sensor fields
        missing fields: dot tracking, microphone direction

        usensors = {}
        byte 9, 10, 11 change with wheel rotation
        usensors["0"] = value[0] & 0x0f
        usensors["1"] = value[1]
        usensors["2"] = value[2]
        usensors["3"] = value[3]
        usensors["4"] = value[4]
        usensors["5"] = value[5]
        usensors["9"] = value[9]  # Changes with wheel rotation
        usensors["10"] = value[10]  # Changes with wheel rotation
        usensors["11"] = value[11]  # Changes with wheel rotation
        print(
            "1:{:08b}\t2:{:08b}\t3:{:08b}\t4:{:08b}\t5:{:08b}"
            .format(value[1], value[2], value[3], value[4], value[5])
        )
        """
