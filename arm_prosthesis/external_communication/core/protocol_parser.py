from enum import Enum
import crc8

from arm_prosthesis.external_communication.core.connectors.request_connector_dto import RequestConnectorDto
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
    _current_request: RequestConnectorDto
    _buffer: bytearray

    def __init__(self):
        self._state = ProtocolState.SFD
        self._payload_size = 0
        self._buffer = bytearray()
        self._crc_calculator = crc8.crc8()

    @property
    def current_request(self) -> RequestConnectorDto:
        return self._current_request

    @property
    def state(self) -> ProtocolState:
        return self._state

    def update(self, data: bytes):
        for byte in data:
            self._buffer.append(byte)

            if self._state is not ProtocolState.SFD and self._state is not ProtocolState.CRC8:
                self._crc_calculator.update(byte.to_bytes(1, 'little'))

            self._update_states()

    def _update_states(self):
        if self.state == ProtocolState.SFD:
            if len(self._buffer) == 8:
                if self._buffer == self._sfd:
                    self._current_request = RequestConnectorDto()
                    self._state = ProtocolState.TYPE
                else:
                    self._buffer.pop(0)
        else:
            if self.state == ProtocolState.TYPE:
                self._current_request.command_type = CommandType(self._buffer[-1])
                self._state = ProtocolState.SIZE
            else:
                if self.state == ProtocolState.SIZE:
                    if len(self._buffer) == 11:
                        self._current_request.payload_size = (self._buffer[-1] << 8) | self._buffer[-2]

                        if self._current_request.payload_size == 0:
                            self._state = ProtocolState.CRC8
                        else:
                            self._state = ProtocolState.PAYLOAD
                else:
                    if self.state == ProtocolState.PAYLOAD:
                        if self._current_request.payload_size + 11 == len(self._buffer):
                            self._current_request.payload = bytes(self._buffer[11:])
                            self._state = ProtocolState.CRC8
                    else:
                        if self.state == ProtocolState.CRC8:
                            self._current_request.received_crc8 = self._buffer[-1].to_bytes(1, 'little')
                            self._current_request.real_crc8 = self._crc_calculator.digest()
                            self._crc_calculator = crc8.crc8()
                            # self._callback_received(self._current_request)
                            self._buffer.clear()
                            self._state = ProtocolState.SFD
                        else:
                            raise Exception('Invalid protocol state')
