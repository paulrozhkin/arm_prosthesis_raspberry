from typing import List

from arm_prosthesis.external_communication.models.dto.entity_dto import EntityDto
from arm_prosthesis.external_communication.models.dto.gesture_dto import GestureDto
from gestures_pb2 import GetGestures


class GetGesturesDto(EntityDto):
    def __init__(self):
        self._last_time_sync = 0
        self._gestures_dto = None

    @property
    def last_time_sync(self) -> int:
        return self._last_time_sync

    @last_time_sync.setter
    def last_time_sync(self, value: int):
        self._last_time_sync = value

    @property
    def gestures_dto(self) -> List[GestureDto]:
        return self._gestures_dto

    @gestures_dto.setter
    def gestures_dto(self, value: List[GestureDto]):
        self._gestures_dto = value

    def serialize(self) -> bytes:
        get_gestures_protobuf = GetGestures()
        get_gestures_protobuf.last_time_sync = self.last_time_sync

        for gesture_dto in self.gestures_dto:
            get_gestures_protobuf.gestures.append(gesture_dto.convert_to_protobuf_gesture())

        return get_gestures_protobuf.SerializeToString()

    def deserialize(self, byte_array: bytes):
        raise NotImplementedError
