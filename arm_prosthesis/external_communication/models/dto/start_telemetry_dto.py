from arm_prosthesis.external_communication.models.dto.entity_dto import EntityDto
from telemetry_pb2 import StartTelemetry


class StartTelemetryDto(EntityDto):
    def __init__(self):
        self._interval_ms = 1

    @property
    def interval_ms(self) -> int:
        return self._interval_ms

    def deserialize(self, byte_array: bytes):
        start_telemetry_protobuf = StartTelemetry()
        start_telemetry_protobuf.ParseFromString(byte_array)
        self._interval_ms = start_telemetry_protobuf.interval_ms

    def serialize(self) -> bytes:
        raise NotImplementedError()
