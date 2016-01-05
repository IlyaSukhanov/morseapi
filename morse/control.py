import pygatt.backends
import time
import logging
import webcolor

DEVICE_HANDLE = 19
COMMANDS={
    "neck_light":0x03,
    "eye_brightness":0x08,
    "eye":0x09,
    "left_ear":0x0b,
    "right_ear":0x0c,
    "head":0x0d
}

class WonderControl(object):
    def __init__(self, address):
        adapter = pygatt.backends.GATTToolBackend()
        adapter.start()
        self.device = adapter.connect(address, address_type='random')

    def command(self, command_name, command_values):
        message = bytearray([COMMANDS[command_name]]) + command_values
        logging.debug([hex(byte) for byte in message])
        self.device.char_write_handle(DEVICE_HANDLE, message)

    def one_byte_array(value):
        return bytearray(struct.pack(">B", value)))

    def two_byte_array(value):
        return bytearray(struct.pack(">H", value)))

    def eye(self, value):
        self.command("eye", two_byte_array(value))

    def eye_brightness(self, value):
        self.command("eye_brightness", one_byte_array(value))

    def neck_light(self, value):
        self.command("neck_light", one_byte_array(value))

if __name__ == "__main__":
    wc = WonderControl("C0:F0:84:3C:51:FA")
    wc.eye(1,1)
    time.sleep(12)
