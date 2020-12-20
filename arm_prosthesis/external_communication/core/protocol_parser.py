from enum import Enum

from datetime import datetime
import crc8

from arm_prosthesis.external_communication.core.connectors.irequest_writer import IPackageReceiver
from arm_prosthesis.external_communication.core.connectors.package_dto import PackageDto
from arm_prosthesis.external_communication.models.command_type import CommandType


class ProtocolState(Enum):
    SFD = 1
    TYPE = 2
    SIZE = 3
    PAYLOAD = 4
    CRC8 = 5


class ProtocolParser:
    _sfd = b'\xfd\xba\xdc\x01\x50\xb4\x11\xff'

    _state: ProtocolState
    _current_package: PackageDto
    _buffer: bytearray
    _last_receive_timestamp: float

    def __init__(self, package_receiver: IPackageReceiver):
        self._state = ProtocolState.SFD
        self._payload_size = 0
        self._buffer = bytearray()
        self._crc_calculator = crc8.crc8()
        self.package_receiver = package_receiver

    @property
    def current_request(self) -> PackageDto:
        return self._current_package

    @property
    def state(self) -> ProtocolState:
        return self._state

    def update(self, data: bytes):
        # Если таймаут приема истек, то сбрасываем буфер и начинаем прием с нуля
        receiver_time = datetime.now().timestamp()
        if self._state != ProtocolState.SFD and receiver_time - self._last_receive_timestamp > 5:
            self._buffer.clear()
            self._state = ProtocolState.SFD
            self._crc_calculator = crc8.crc8()

        for byte in data:
            self._buffer.append(byte)

            if self._state is not ProtocolState.SFD and self._state is not ProtocolState.CRC8:
                self._crc_calculator.update(byte.to_bytes(1, 'little'))

            self._update_states()

        self._last_receive_timestamp = receiver_time

    def _update_states(self):
        if self.state == ProtocolState.SFD:
            if len(self._buffer) == 8:
                if self._buffer == self._sfd:
                    self._current_package = PackageDto()
                    self._state = ProtocolState.TYPE
                else:
                    self._buffer.pop(0)
        else:
            if self.state == ProtocolState.TYPE:
                self._current_package.command_type = CommandType(self._buffer[-1])
                self._state = ProtocolState.SIZE
            else:
                if self.state == ProtocolState.SIZE:
                    if len(self._buffer) == 11:
                        self._current_package.payload_size = (self._buffer[-1] << 8) | self._buffer[-2]

                        if self._current_package.payload_size == 0:
                            self._state = ProtocolState.CRC8
                        else:
                            self._state = ProtocolState.PAYLOAD
                else:
                    if self.state == ProtocolState.PAYLOAD:
                        if self._current_package.payload_size + 11 == len(self._buffer):
                            self._current_package.payload = bytes(self._buffer[11:])
                            self._state = ProtocolState.CRC8
                    else:
                        if self.state == ProtocolState.CRC8:
                            self._current_package.received_crc8 = self._buffer[-1].to_bytes(1, 'little')
                            self._current_package.real_crc8 = self._crc_calculator.digest()
                            self._crc_calculator = crc8.crc8()

                            self.package_receiver.receive_package(self._current_package)

                            self._buffer.clear()
                            self._state = ProtocolState.SFD
                        else:
                            raise Exception('Invalid protocol state')

    @staticmethod
    def create_package(command_type: CommandType, payload: bytes) -> PackageDto:
        package = PackageDto()

        package.command_type = command_type

        if payload is None:
            package.payload_size = 0
        else:
            package.payload_size = len(payload)
            package.payload = payload

        return package

    def serialize_package(self, package: PackageDto):
        ser_package = bytearray()
        package_crc_calculator = crc8.crc8()

        ser_package.extend(self._sfd)
        ser_package.append(package.command_type.value)
        ser_package.extend(package.payload_size.to_bytes(2, 'little'))

        if package.payload_size != 0:
            ser_package.extend(package.payload)

        package_crc_calculator.update(ser_package[8:])
        crc = package_crc_calculator.digest()
        ser_package.extend(crc)

        return ser_package
