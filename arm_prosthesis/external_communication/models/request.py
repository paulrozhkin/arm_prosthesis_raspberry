from arm_prosthesis.external_communication.core.connectors.iresponse_writer import IResponseWriter
from arm_prosthesis.external_communication.models.command_type import CommandType


class Request:
    def __init__(self, command_type: CommandType, payload: bytes, response_writer: IResponseWriter):
        self._command_type = command_type
        self._payload = payload
        self._response_writer = response_writer

    @property
    def command_type(self) -> CommandType:
        return self._command_type

    @property
    def payload(self) -> bytes:
        return self._payload

    @property
    def response_writer(self) -> IResponseWriter:
        return self._response_writer
