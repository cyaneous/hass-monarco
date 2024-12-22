"""Structures used by the monarco_hat library."""

import struct
from collections import namedtuple


# Define the SDC structure
MonarcoStructSDC = namedtuple('MonarcoStructSDC', 'value address write error reserved')
MonarcoStructControlByte = namedtuple('MonarcoStructControlByte', 'status_led_mask status_led_value ow_shutdown reserved1 cnt1_reset cnt2_reset sign_of_life_a sign_of_life_b')
MonarcoStructControlByteFormat = 'BBBBBBBB'

# Define the TX structure
class MonarcoStructTX:
    def __init__(self):
        self.sdc_req = MonarcoStructSDC(0, 0, 0, 0, 0)
        self.control_byte = MonarcoStructControlByte(0, 0, 0, 0, 0, 0, 0, 0)
        self.led_mask = 0
        self.led_value = 0
        self.dout = 0
        self.pwm1_div = 0
        self.pwm1a_dc = 0
        self.pwm1b_dc = 0
        self.pwm1c_dc = 0
        self.pwm2_div = 0
        self.pwm2a_dc = 0
        self.aout1 = 0
        self.aout2 = 0
        self.crc = 0

    def pack(self):
        return struct.pack('<HHBBBBHHHHHHHHH', 
            self.sdc_req.value, 
            (self.sdc_req.address & 0xFFF) | (self.sdc_req.write << 12) | (self.sdc_req.error << 13) | (self.sdc_req.reserved << 14), 
            self.control_byte.status_led_mask | (self.control_byte.status_led_value << 1) | (self.control_byte.ow_shutdown << 2) | (self.control_byte.reserved1 << 3) | (self.control_byte.cnt1_reset << 4) | (self.control_byte.cnt2_reset << 5) | (self.control_byte.sign_of_life_a << 6) | (self.control_byte.sign_of_life_b << 7),
            self.led_mask, 
            self.led_value, 
            self.dout, 
            self.pwm1_div, 
            self.pwm1a_dc, 
            self.pwm1b_dc, 
            self.pwm1c_dc, 
            self.pwm2_div, 
            self.pwm2a_dc, 
            self.aout1, 
            self.aout2, 
            self.crc
        )


# Define the RX structure
class MonarcoStructRX:
    def __init__(self):
        self.sdc_resp = MonarcoStructSDC(0, 0, 0, 0, 0)
        self.status_byte = 0
        self.din = 0
        self.cnt1 = 0
        self.cnt2 = 0
        self.cnt3 = 0
        self.ain1 = 0
        self.ain2 = 0
        self.crc = 0

    def unpack(self, data):
        unpacked_data = struct.unpack('<HHBHBIIIHHH', data)
        self.sdc_resp = MonarcoStructSDC(unpacked_data[0], unpacked_data[1] & 0xFFF, (unpacked_data[1] >> 12) & 1, (unpacked_data[1] >> 13) & 1, (unpacked_data[1] >> 14) & 3)
        self.status_byte, _, self.din, self.cnt1, self.cnt2, self.cnt3, self.ain1, self.ain2, self.crc = unpacked_data[2:]

# Define SDC Item structure
class MonarcoSDCItem:
    def __init__(self, address=0, value=0, factor=0, write=0, request=0, done=0, error=0):
        self.address = address
        self.value = value
        self.factor = factor
        self.counter = 0
        self.busy = 0
        self.write = write
        self.request = request
        self.done = done
        self.error = error