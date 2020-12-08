from typing import List

from arm_prosthesis.external_communication.models.dto.entity_dto import EntityDto
from arm_prosthesis.external_communication.models.dto.gesture_action_dto import GestureActionDto
from gestures_pb2 import Gesture, GestureAction


class GestureDto(EntityDto):
    def __init__(self):
        self._id: str = ''
        self._name: str = ''
        self._last_time_sync: int = 0
        self._iterable = False
        self._repetitions = 0
        self._actions: List[GestureActionDto] = []

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def last_time_sync(self) -> int:
        return self._last_time_sync

    @property
    def iterable(self) -> bool:
        return self._iterable

    @property
    def repetitions(self) -> int:
        return self._repetitions

    @property
    def actions(self) -> List[GestureActionDto]:
        return self._actions

    def create_from_protobuf_gesture(self, gesture_proto: Gesture):
        self._id = gesture_proto.id.value
        self._name = gesture_proto.name
        self._last_time_sync = gesture_proto.last_time_sync
        self._iterable = gesture_proto.iterable
        self._repetitions = gesture_proto.repetitions

        self._actions.clear()
        for action_protobuf in gesture_proto.actions:
            gesture = GestureActionDto()
            gesture.create_from_protobuf_action(action_protobuf)
            self._actions.append(gesture)

    def serialize(self) -> bytes:
        pass

    def deserialize(self, byte_array: bytes):
        pass
