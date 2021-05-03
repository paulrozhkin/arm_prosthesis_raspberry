from arm_prosthesis.external_communication.models.dto.entity_dto import EntityDto
from patterns_pb2 import MioPattern


class MioPatternDto(EntityDto):
    def __init__(self):
        self._pattern: int = 0
        self._gesture_id: str = ''

    @property
    def gesture_id(self) -> str:
        return self._gesture_id

    @gesture_id.setter
    def gesture_id(self, value: str):
        self._gesture_id = value

    @property
    def pattern(self) -> int:
        return self._pattern

    @pattern.setter
    def pattern(self, value: int):
        self._pattern = value

    def create_from_protobuf_pattern(self, mio_pattern_proto: MioPattern):
        self._pattern = mio_pattern_proto.pattern
        self._gesture_id = mio_pattern_proto.gesture_id.value

    def convert_to_protobuf_pattern(self) -> MioPattern:
        mio_pattern_proto = MioPattern()
        mio_pattern_proto.gesture_id.value = self.gesture_id
        mio_pattern_proto.pattern = self.pattern

        return mio_pattern_proto

    def serialize(self) -> bytes:
        pattern_proto = self.convert_to_protobuf_pattern()
        return pattern_proto.SerializeToString()

    def deserialize(self, byte_array: bytes):
        mio_pattern_proto = MioPattern()
        mio_pattern_proto.ParseFromString(byte_array)
        self.create_from_protobuf_pattern(mio_pattern_proto)
