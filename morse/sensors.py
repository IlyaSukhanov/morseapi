import logging
from constants import CHARACTERISTICS

class MorseSense(object):
    def __init__(self, connection, state, robot_type):
        """
        Enable Robot sensors, writing results back into state dict

        :param connection: pygatt device connectio
        :param state: robot state dict
        :roboto type: type of robot: "dot"|"dash"
        """
        self.state = state
        self.robot_type = robot_type
        self.connection = connection
        self.ready = False
        self.start()
        while not self.ready:
            pass

    def start(self):
        if self.robot_type == "dash":
            self.connection.subscribe(CHARACTERISTICS["dash_sensor"], self._dash_sensor_decode)

    def _dash_sensor_decode(self, handle, value):
        self.ready = True
        self.state["dash_index"] = value[0] >> 4
        self.state["prox_right"] = value[6]
        self.state["prox_left"] = value[7]
        self.state["prox_rear"] = value[8]
        self.state["robot_yaw"] = (value[13] << 8) | value[12]
        self.state["left_wheel"] = (value[15] << 8) | value[14]
        self.state["right_wheel"] = (value[17] << 8) | value[16]
        self.state["head_pitch"] = value[18]
        self.state["head_yaw"] = value[19]
        logging.debug("self.state: {}".format(self.state))
        """
        Unknown sensor fields

        usensors = {}
        byte 9, 10, 11 change with wheel rotation
        usensors["0"] = value[0] & 0x0f
        usensors["1"] = value[1]
        usensors["2"] = value[2]
        usensors["3"] = value[3]
        usensors["4"] = value[4]
        usensors["5"] = value[5]
        print("1:{:08b}\t2:{:08b}\t3:{:08b}\t4:{:08b}\t5:{:08b}".format(value[1], value[2], value[3], value[4], value[5]))
        """
