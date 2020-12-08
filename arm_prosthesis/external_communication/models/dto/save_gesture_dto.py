from arm_prosthesis.external_communication.models.dto.entity_dto import EntityDto
from arm_prosthesis.external_communication.models.dto.gesture_dto import GestureDto
from gestures_pb2 import SaveGesture


class SaveGestureDto(EntityDto):

    def __init__(self):
        self._time_sync = 0
        self._gesture_dto = None

    @property
    def time_sync(self) -> int:
        return self._time_sync

    @property
    def gesture_dto(self) -> GestureDto:
        return self._gesture_dto

    def serialize(self) -> bytes:
        raise NotImplementedError

    def deserialize(self, byte_array: bytes):
        save_gesture_protobuf = SaveGesture()
        save_gesture_protobuf.ParseFromString(byte_array)

        self._time_sync = save_gesture_protobuf.time_sync
        self._gesture_dto = GestureDto()
        self._gesture_dto.create_from_protobuf_gesture(save_gesture_protobuf.gesture)
