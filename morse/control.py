import pygatt.backends
import time

DEVICE_HANDLE = 19
COMMANDS={"neck":0x03, "eye":0x08, "left_ear":0x0b, "right_ear":0x0c, "head":0x0d}

class WonderControl(object):
    def __init__(self, address):
        adapter = pygatt.backends.GATTToolBackend()
        adapter.start()
        self.device = adapter.connect(address, address_type='random')

    def command(self, command_name, command_value):
        #message = bytearray(COMMANDS[command_name])
        #message.append(command_value)
        self.device.char_write_handle(DEVICE_HANDLE, bytearray(COMMANDS[command_name]) + command_value)

    def eye(self, value1, value2):
        self.command("eye", bytearray([value1, value2]))

if __name__ == "__main__":
    wc = WonderControl("C0:F0:84:3C:51:FA")
    wc.eye(1,1)
    time.sleep(12)
