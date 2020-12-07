from arm_prosthesis.external_communication.models.command_type import CommandType


class RequestConnectorDto:
    _command_type: CommandType
    _payload_size: int
    _payload: bytes
    _received_crc8: int
    _real_crc8: int

    @property
    def command_type(self) -> CommandType:
        return self._command_type

    @command_type.setter
    def command_type(self, var: CommandType):
        self._command_type = var

    @property
    def payload_size(self) -> int:
        return self._payload_size

    @payload_size.setter
    def payload_size(self, var: int):
        self._payload_size = var

    @property
    def payload(self) -> bytes:
        return self._payload

    @payload.setter
    def payload(self, var: bytes):
        self._payload = var

    @property
    def received_crc8(self) -> int:
        return self._received_crc8

    @received_crc8.setter
    def received_crc8(self, var: int):
        self._received_crc8 = var

    @property
    def real_crc8(self) -> int:
        return self._real_crc8

    @real_crc8.setter
    def real_crc8(self, var: int):
        self._real_crc8 = var
