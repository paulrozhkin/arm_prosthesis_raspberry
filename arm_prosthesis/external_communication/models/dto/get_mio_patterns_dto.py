from typing import List

from arm_prosthesis.external_communication.models.dto.entity_dto import EntityDto
from arm_prosthesis.external_communication.models.dto.mio_pattern_dto import MioPatternDto
from patterns_pb2 import GetMioPatterns


class GetMioPatternsDto(EntityDto):
    def __init__(self):
        self._patterns_dto = None

    @property
    def patterns_dto(self) -> List[MioPatternDto]:
        return self._patterns_dto

    @patterns_dto.setter
    def patterns_dto(self, value: List[MioPatternDto]):
        self._patterns_dto = value

    def serialize(self) -> bytes:
        get_mio_patterns_protobuf = GetMioPatterns()

        for gesture_dto in self.patterns_dto:
            get_mio_patterns_protobuf.patterns.append(gesture_dto.convert_to_protobuf_pattern())

        return get_mio_patterns_protobuf.SerializeToString()

    def deserialize(self, byte_array: bytes):
        raise NotImplementedError
