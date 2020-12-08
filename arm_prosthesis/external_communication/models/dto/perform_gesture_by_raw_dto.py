from arm_prosthesis.external_communication.models.dto.entity_dto import EntityDto
from arm_prosthesis.external_communication.models.dto.gesture_dto import GestureDto
from gestures_pb2 import PerformGestureRaw


class PerformGestureRawDto(EntityDto):

    def __init__(self):
        self._gesture_dto = None

    @property
    def gesture_dto(self) -> GestureDto:
        return self._gesture_dto

    def serialize(self) -> bytes:
        raise NotImplementedError

    def deserialize(self, byte_array: bytes):
        perform_gesture_protobuf = PerformGestureRaw()
        perform_gesture_protobuf.ParseFromString(byte_array)

        self._gesture_dto = GestureDto()
        self._gesture_dto.create_from_protobuf_gesture(perform_gesture_protobuf.gesture)
