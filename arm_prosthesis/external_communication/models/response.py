from arm_prosthesis.external_communication.models.command_type import CommandType


class Response:
    def __init__(self, command_type: CommandType, payload: bytearray = None):
        self._command_type = command_type
        self._payload = payload

    @property
    def command_type(self) -> CommandType:
        return self._command_type

    @property
    def payload(self) -> bytearray:
        return self._payload
