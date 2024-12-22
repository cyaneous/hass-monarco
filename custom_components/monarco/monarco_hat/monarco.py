"""Implementation of the monarco_hat library."""

import logging
import struct

import spidev

from .const import CRC16_TABLE
from .exceptions import MHConnectionException, MHRuntimeException, MHTimeoutException
from .structures import MonarcoStructSDC, MonarcoSDCItem, MonarcoStructTX, MonarcoStructRX

_LOGGER = logging.getLogger(__name__)

MONARCO_SDC_ITEMS_SIZE = 256


class Monarco:
    def __init__(self, spi_device = "0.0", spi_clkfreq = 400000):
        self._tx_data = MonarcoStructTX()
        self._rx_data = MonarcoStructRX()
        self._spi_fd = None
        self._sdc_size = 0
        self._sdc_idx = 0
        self._sdc_items = [MonarcoSDCItem() for _ in range(MONARCO_SDC_ITEMS_SIZE)]

        self._open(spi_device, spi_clkfreq)
        _LOGGER.info("monarco_init: OK")

    def _open(self, spi_device, spi_clkfreq) -> None:
        """Opens the SPI interface connection."""

        self._spi_fd = spidev.SpiDev()
        bus, device = map(int, spi_device.split('.'))
        self._spi_fd.open(bus, device)
        
        if not self._spi_fd:
            raise MHConnectionException("Failed to open the SPI interface")
        
        self._spi_fd.max_speed_hz = spi_clkfreq
        self._spi_fd.mode = 0b00
        self._spi_fd.bits_per_word = 8

    def close(self):
        """Closes the SPI interface connection."""
        
        if self._spi_fd:
            self._spi_fd.close()
            self._spi_fd = None

    def run(self) -> int:
        """Runs the main send and receive functionality."""
        
        if not self._spi_fd:
            raise MHRuntimeException("SPI is not open")

        self._sdc_tx()

        tx_data = self._tx_data.pack()
        self._tx_data.crc = self._monarco_crc16(tx_data[:24])
        tx_data = self._tx_data.pack()

        # _LOGGER.debug("TX: %s", tx_data.hex())
        rx_data = bytes(self._spi_fd.xfer(tx_data))

        # _LOGGER.debug("RX: %s", rx_data.hex())
        if struct.unpack_from('<H', rx_data, 24)[0] != self._monarco_crc16(rx_data[:24]):
            raise MHRuntimeException("Invalid RX CRC")

        self._rx_data.unpack(rx_data)
        self._sdc_rx()

        return 0

    def _sdc_tx(self):
        """Writes SDC."""

        idx_last = self._sdc_idx

        if self._sdc_idx >= self._sdc_size:
            return

        item = self._sdc_items[self._sdc_idx]

        if item.busy > 0:
            if item.busy < (1 << 31):
                item.busy += 1
            if item.busy == 10:
                raise MHTimeoutException(f"_sdc_tx: SDC item {self._sdc_idx} {'W' if item.write else 'R'} ADDR=0x{item.address:03X} timeout")

        while True:
            if self._sdc_items[self._sdc_idx].factor > 0:
                self._sdc_items[self._sdc_idx].counter += 1
                if self._sdc_items[self._sdc_idx].counter == self._sdc_items[self._sdc_idx].factor:
                    self._sdc_items[self._sdc_idx].counter = 0
                    break

            if self._sdc_items[self._sdc_idx].request != 0:
                break

            self._sdc_idx += 1
            if self._sdc_idx >= self._sdc_size:
                self._sdc_idx = 0

            if self._sdc_idx == idx_last:
                raise MHRuntimeException(f"_sdc_tx: No SDC request in this cycle")

        item = self._sdc_items[self._sdc_idx]

        self._tx_data.sdc_req = MonarcoStructSDC(item.value, item.address, item.write, 0, 0)
        item.busy = 1
        item.request = 0

    def _sdc_rx(self):
        """Reads SDC."""
        
        if self._sdc_idx >= self._sdc_size:
            return

        item = self._sdc_items[self._sdc_idx]

        if self._rx_data.sdc_resp.address != item.address or self._rx_data.sdc_resp.write != item.write:
            return

        if self._rx_data.sdc_resp.write == 1 and self._rx_data.sdc_resp.error == 0 and self._rx_data.sdc_resp.value != item.value:
            return

        if self._rx_data.sdc_resp.error and (not item.error or item.value != self._rx_data.sdc_resp.value):
            raise MHRuntimeException(f"_sdc_rx: SDC item {self._sdc_idx} {'W' if item.write else 'R'} ADDR=0x{item.address:03X} ERROR=0x{self._rx_data.sdc_resp.value:03X}")

        item.busy = 0
        item.done = 1
        item.value = self._rx_data.sdc_resp.value
        item.error = self._rx_data.sdc_resp.error

        self._sdc_idx += 1
        if self._sdc_idx == self._sdc_size:
            self._sdc_idx = 0

    def _monarco_crc16(self, data) -> int:
        """Modbus CRC-16 calculation using a table."""

        crc = 0xFFFF
        for byte in data:
            crc = (crc >> 8) ^ CRC16_TABLE[(byte ^ crc) & 0xFF]
        return crc
