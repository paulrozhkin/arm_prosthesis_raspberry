from arm_prosthesis.external_communication.models.dto.entity_dto import EntityDto
from gestures_pb2 import DeleteGesture


class DeleteGestureDto(EntityDto):

    def __init__(self):
        self._time_sync = 0
        self._id = ''

    @property
    def time_sync(self) -> int:
        return self._time_sync

    @property
    def id(self) -> str:
        return self._id

    def serialize(self) -> bytes:
        raise NotImplementedError

    def deserialize(self, byte_array: bytes):
        delete_gesture_protobuf = DeleteGesture()
        delete_gesture_protobuf.ParseFromString(byte_array)

        self._time_sync = delete_gesture_protobuf.time_sync
        self._id = delete_gesture_protobuf.id.value
