from typing import List

from arm_prosthesis.external_communication.models.dto.entity_dto import EntityDto
from arm_prosthesis.external_communication.models.dto.mio_pattern_dto import MioPatternDto
from patterns_pb2 import SetMioPatterns


class SetMioPatternsDto(EntityDto):
    def __init__(self):
        self._patterns_dto = None

    @property
    def patterns_dto(self) -> List[MioPatternDto]:
        return self._patterns_dto

    @patterns_dto.setter
    def patterns_dto(self, value: List[MioPatternDto]):
        self._patterns_dto = value

    def serialize(self) -> bytes:
        set_mio_patterns_protobuf = SetMioPatterns()

        for pattern_dto in self._patterns_dto:
            set_mio_patterns_protobuf.patterns.append(pattern_dto.convert_to_protobuf_pattern())

        return set_mio_patterns_protobuf.SerializeToString()

    def deserialize(self, byte_array: bytes):
        set_mio_patterns_protobuf = SetMioPatterns()
        set_mio_patterns_protobuf.ParseFromString(byte_array)

        self.patterns_dto = []
        for pattern_protobuf in set_mio_patterns_protobuf.patterns:
            pattern_dto = MioPatternDto()
            pattern_dto.create_from_protobuf_pattern(pattern_protobuf)
            self.patterns_dto.append(pattern_dto)
