"""Structures used by the monarco_hat library."""

import struct


class MonarcoStructSDC:
    def __init__(self, value=0, address=0, write=0, error=0):
        self.value = value
        self.address = address
        self.write = write
        self.error = error


class MonarcoStructControlByte:
    def __init__(self, u8=0):
        self.u8 = u8


class MonarcoStructTX:
    def __init__(self):
        self.sdc_req = MonarcoStructSDC()
        self.control_byte = MonarcoStructControlByte()
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


class MonarcoStructRX:
    def __init__(self):
        self.sdc_resp = MonarcoStructSDC()
        self.status_byte = MonarcoStructControlByte()
        self.din = 0
        self.cnt1 = 0
        self.cnt2 = 0
        self.cnt3 = 0
        self.ain1 = 0
        self.ain2 = 0
        self.crc = 0
