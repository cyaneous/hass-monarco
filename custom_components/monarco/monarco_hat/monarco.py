"""Implementation of the monarco_hat library."""

import spidev
import struct

from .const import CRC16_TABLE


MONARCO_SDC_ITEMS_SIZE = 256

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

class MonarcoContext:
    def __init__(self, platform=None):
        self.platform = platform
        self.tx_data = bytearray(26)
        self.rx_data = bytearray(26)
        self.spi_fd = None
        self.sdc_size = 0
        self.sdc_idx = 0
        self.sdc_items = [MonarcoSDCItem() for _ in range(MONARCO_SDC_ITEMS_SIZE)]
        self.err_throttle_crc = 0

    def open_spi_device(self, spi_device, spi_clkfreq):
        self.spi_fd = spidev.SpiDev()
        bus, device = map(int, spi_device.split('.'))
        self.spi_fd.open(bus, device)
        self.spi_fd.max_speed_hz = spi_clkfreq
        self.spi_fd.mode = 0b00
        self.spi_fd.bits_per_word = 8

    def close_spi_device(self):
        if self.spi_fd:
            self.spi_fd.close()

def monarco_crc16(data):
    crc = 0xFFFF
    for byte in data:
        crc = (crc >> 8) ^ CRC16_TABLE[(crc ^ byte) & 0xFF]
    return crc

def monarco_init(cxt, spi_device, spi_clkfreq, platform):
    cxt.platform = platform
    cxt.tx_data = bytearray(26)
    cxt.rx_data = bytearray(26)
    cxt.sdc_size = 0
    cxt.sdc_idx = 0
    cxt.err_throttle_crc = 0

    cxt.open_spi_device(spi_device, spi_clkfreq)
    print("monarco_init: OK")

def monarco_main(cxt):
    if not cxt.spi_fd:
        print("monarco_main: SPI not open, exiting")
        return -1

    monarco_sdc_tx(cxt)

    tx_data = cxt.tx_data
    tx_data_crc = monarco_crc16(tx_data[:24])
    struct.pack_into('<H', tx_data, 24, tx_data_crc)

    rx_data = cxt.spi_fd.xfer2(tx_data)

    if struct.unpack_from('<H', rx_data, 24)[0] != monarco_crc16(rx_data[:24]):
        if cxt.err_throttle_crc == 0:
            print("monarco_main: Invalid RX CRC")
        if cxt.err_throttle_crc < (1 << 31):
            cxt.err_throttle_crc += 1
        return -3
    else:
        if cxt.err_throttle_crc:
            print(f"monarco_main: Invalid RX CRC ({cxt.err_throttle_crc} times)")
            cxt.err_throttle_crc = 0

    cxt.rx_data = rx_data
    monarco_sdc_rx(cxt)

    return 0

def monarco_sdc_tx(cxt):
    idx_last = cxt.sdc_idx

    if cxt.sdc_idx >= cxt.sdc_size:
        return

    item = cxt.sdc_items[cxt.sdc_idx]

    if item.busy > 0:
        if item.busy < (1 << 31):
            item.busy += 1
        if item.busy == 10:
            print(f"monarco_sdc_tx: SDC item {cxt.sdc_idx} {'W' if item.write else 'R'} ADDR=0x{item.address:03X} timeout")
        return

    while True:
        if cxt.sdc_items[cxt.sdc_idx].factor > 0:
            cxt.sdc_items[cxt.sdc_idx].counter += 1
            if cxt.sdc_items[cxt.sdc_idx].counter == cxt.sdc_items[cxt.sdc_idx].factor:
                cxt.sdc_items[cxt.sdc_idx].counter = 0
                break

        if cxt.sdc_items[cxt.sdc_idx].request != 0:
            break

        cxt.sdc_idx += 1
        if cxt.sdc_idx >= cxt.sdc_size:
            cxt.sdc_idx = 0

        if cxt.sdc_idx == idx_last:
            print("monarco_sdc_tx: No SDC request in this cycle")
            return

    item = cxt.sdc_items[cxt.sdc_idx]

    cxt.tx_data[0:2] = struct.pack('<H', item.value)
    cxt.tx_data[2] = item.address & 0xFF
    cxt.tx_data[3] = ((item.address >> 8) & 0x0F) | (item.write << 4) | (item.error << 5)

    item.busy = 1
    item.request = 0

def monarco_sdc_rx(cxt):
    if cxt.sdc_idx >= cxt.sdc_size:
        return

    item = cxt.sdc_items[cxt.sdc_idx]

    if struct.unpack_from('<H', cxt.rx_data, 2)[0] != item.address or \
       ((cxt.rx_data[3] & 0x10) >> 4) != item.write:
        return

    if item.write == 1 and cxt.rx_data[0:2] != struct.pack('<H', item.value):
        return

    if (cxt.rx_data[3] & 0x20) and (not item.error or item.value != struct.unpack_from('<H', cxt.rx_data, 4)[0]):
        print(f"monarco_sdc_rx: SDC item {cxt.sdc_idx} {'W' if item.write else 'R'} ADDR=0x{item.address:03X} ERROR=0x{cxt.rx_data[4:6].hex()}")

    item.busy = 0
    item.done = 1
    item.value = struct.unpack_from('<H', cxt.rx_data, 4)[0]
    item.error = (cxt.rx_data[3] & 0x20) >> 5

    cxt.sdc_idx += 1
    if cxt.sdc_idx == cxt.sdc_size:
        cxt.sdc_idx = 0

def monarco_exit(cxt):
    cxt.close_spi_device()
    print("monarco_exit: OK")
