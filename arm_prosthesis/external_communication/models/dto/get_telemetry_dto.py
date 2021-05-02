from arm_prosthesis.external_communication.models.dto.entity_dto import EntityDto
from arm_prosthesis.external_communication.models.dto.telemetry_dto import TelemetryDto
from telemetry_pb2 import GetTelemetry


class GetTelemetryDto(EntityDto):
    def __init__(self):
        self._telemetry = None

    @property
    def telemetry(self) -> TelemetryDto:
        return self._telemetry

    @telemetry.setter
    def telemetry(self, value: TelemetryDto):
        self._telemetry = value

    def serialize(self) -> bytes:
        get_telemetry_protobuf = GetTelemetry()
        get_telemetry_protobuf.telemetry = self.telemetry.convert_to_protobuf_gesture()

        return get_telemetry_protobuf.SerializeToString()

    def deserialize(self, byte_array: bytes):
        raise NotImplementedError
