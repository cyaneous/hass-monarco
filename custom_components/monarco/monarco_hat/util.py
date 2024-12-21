"""Utilities used by the monarco_hat library."""

import math

MONARCO_ADC_RANGE = 4095
MONARCO_ADC_10V_RANGE = 10.0
MONARCO_ADC_20MA_RANGE = 52.475

def pwm_freq_to_u16(freq_hz):
    if freq_hz < 1:
        return 0
    elif freq_hz < 10:
        return 3 + (round(32000000 / 512 / freq_hz) & 0xFFFC)
    elif freq_hz < 100:
        return 2 + (round(32000000 / 64 / freq_hz) & 0xFFFC)
    elif freq_hz < 1000:
        return 1 + (round(32000000 / 8 / freq_hz) & 0xFFFC)
    elif freq_hz < 100000:
        return 0 + (round(32000000 / 1 / freq_hz) & 0xFFFC)
    else:
        return 0

def pwm_dc_to_u16(dc):
    if dc <= 0:
        return 0
    elif dc >= 1:
        return 65535
    else:
        return round(65535 * dc)

def aout_volts_to_u16(volts):
    if volts < 0:
        return 0
    elif volts > 10:
        return MONARCO_ADC_RANGE
    else:
        return round(volts / MONARCO_ADC_10V_RANGE * MONARCO_ADC_RANGE)

def ain_10v_to_real(ain):
    return ain * MONARCO_ADC_10V_RANGE / MONARCO_ADC_RANGE

def ain_20ma_to_real(ain):
    return ain * MONARCO_ADC_20MA_RANGE / MONARCO_ADC_RANGE

def dump_tx(tx):
    print(f"TX: SDC[V:0x{tx.sdc_req.value:04X} A:0x{tx.sdc_req.address:03X} W:{tx.sdc_req.write} E:{tx.sdc_req.error}] "
          f"CTRL:0x{tx.control_byte.u8:02X} LED_MASK:0x{tx.led_mask:02X} LED_VALUE:0x{tx.led_value:02X} "
          f"DO:0x{tx.dout:1X} PWM1DIV:0x{tx.pwm1_div:02X} PWM1A:0x{tx.pwm1a_dc:02X} PWM1B:0x{tx.pwm1b_dc:02X} "
          f"PWM1C:0x{tx.pwm1c_dc:02X} PWM2DIV:0x{tx.pwm2_div:02X} PWM2A:0x{tx.pwm2a_dc:02X} AO1:0x{tx.aout1:02X} "
          f"AO2:0x{tx.aout2:02X} CRC:0x{tx.crc:04X}")

def dump_rx(rx):
    print(f"RX: SDC[V:0x{rx.sdc_resp.value:04X} A:0x{rx.sdc_resp.address:03X} W:{rx.sdc_resp.write} E:{rx.sdc_resp.error}] "
          f"STAT:0x{rx.status_byte.u8:02X} DI:0x{rx.din:1X} CNT1:0x{rx.cnt1:04X} CNT2:0x{rx.cnt2:04X} "
          f"CNT3:0x{rx.cnt3:04X} AI1:0x{rx.ain1:04X} AI2:0x{rx.ain2:04X} CRC:0x{rx.crc:04X}")
