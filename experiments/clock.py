import time
import pexpect
import datetime

class WonderClockFace(object):
    def __init__(self, mac_address):
        self.connection = pexpect.spawnu("gatttool -t random -b {0} -I".format(mac_address))
        self.connection.sendline('connect')

    def eye(self, value):
        hex_value = hex(value).split('x')[1]
        print('char-write-cmd 0x0013 09{:0>4s}'.format(hex_value))
        self.connection.sendline('char-write-cmd 0x0013 08fb09{:0>4s}'.format(hex_value))

    def draw(self, hour, minute, duration=.25):
        end_time = time.time() + duration
        if hour == 0:
            hour_value = 0
        else:
            hour_value = (1<<hour)

        if minute == 0:
            minute_value = 0
        else:
            minute_value = (1<<minute)

        while time.time() < end_time:
            for _ in range(0,4):
                self.eye(hour_value)
                time.sleep(.1)
                self.eye(hour_value|minute_value)
                time.sleep(.1)

    def run(self):
        while True:
            self.draw(datetime.datetime.now().hour % 12, datetime.datetime.now().minute * 12 / 60)

if __name__ == "__main__":
    wcf = WonderClockFace("C0:F0:84:3C:51:FA")
    wcf.run()
