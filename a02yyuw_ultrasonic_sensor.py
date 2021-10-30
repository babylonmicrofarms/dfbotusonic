import serial  # type: ignore
import time
from enum import IntEnum
from typing import NamedTuple


class Status(IntEnum):
    OK = 0x00
    ERR_CHECKSUM = 0x01
    ERR_SERIAL = 0x02
    ERR_ABOVE_MAX_LIMIT = 0x03
    ERR_BELOW_MIN_LIMIT = 0x04
    ERR_DATA = 0x05
    ERR_HEADER = 0x06


class SerialData(NamedTuple):
    header: int
    distance_high_byte: int
    distance_low_byte: int
    checksum: int


class HeaderByteError(Exception):
    pass


class DataError(Exception):
    pass


class A02YYUWUltrasonicSensor:
    distance_max = 4500
    distance_min = 0
    _status = Status.OK
    _distance = 0
    _exp_len_ser_data = len(SerialData._fields)
    _req_header_byte = 0xFF

    def __init__(self, dev_id: str):
        self.ser = serial.Serial(dev_id, 9600)
        if self.ser.isOpen() != True:
            self._status = Status.ERR_SERIAL

    @property
    def distance(self) -> int:
        return self._distance

    @property
    def status(self) -> Status:
        return self._status

    def read(self):
        try:
            data = self._read_serial_data()
            checksum = self._calc_checksum(data)
            self._distance = data.distance_high_byte * 256 + data.distance_low_byte
            if checksum != data.checksum:
                self._status = Status.ERR_CHECKSUM
                return

            if self._distance > self.distance_max:
                self._status = Status.ERR_ABOVE_MAX_LIMIT
                self._distance = self.distance_max
                return

            if self._distance < self.distance_min:
                self._status = Status.ERR_BELOW_MIN_LIMIT
                self._distance = self.distance_min
                return

            self._status = Status.OK

        except HeaderByteError:
            self._status = Status.ERR_HEADER

        except DataError:
            self._status = Status.ERR_DATA

        finally:
            # seems to clear the internal sensor buffer so new readings propagate correctly
            self.ser.read(self.ser.inWaiting())

    def set_distance_range(self, min: int, max: int):
        self.distance_max = max
        self.distance_min = min

    def _read_serial_data(self) -> SerialData:
        self._warmup_serial_com()
        data = []
        max_retries = 10
        retries = 0
        i = 0

        while self.ser.inWaiting() > 0:
            if retries >= max_retries:
                raise HeaderByteError()

            serial_byte = self.ser.read()
            data_byte = ord(serial_byte)
            if i == 0:
                is_header_bad = data_byte != self._req_header_byte
                if is_header_bad:
                    retries += 1
                    continue

            data.append(data_byte)
            i += 1
            if i >= self._exp_len_ser_data:
                break

        if len(data) != self._exp_len_ser_data:
            raise DataError()

        return SerialData(data[0], data[1], data[2], data[3])

    def _warmup_serial_com(self):
        i = 0
        while self.ser.inWaiting() == 0:
            i += 1
            time.sleep(0.05)
            if i > self._exp_len_ser_data:
                break

    def _calc_checksum(self, data: SerialData) -> int:
        return (data.header + data.distance_high_byte + data.distance_low_byte) & 0xFF
