from arm_prosthesis.external_communication.models.dto.entity_dto import EntityDto
from gestures_pb2 import SetPositions


class SetPositionsDto(EntityDto):

    def __init__(self):
        self._little_finger_position = 0
        self._ring_finger_position = 0
        self._middle_finger_position = 0
        self._index_finger_position = 0
        self._thumb_finger_position = 0

    @property
    def little_finger_position(self) -> int:
        return self._little_finger_position

    @property
    def ring_finger_position(self) -> int:
        return self._ring_finger_position

    @property
    def middle_finger_position(self) -> int:
        return self._middle_finger_position

    @property
    def index_finger_position(self) -> int:
        return self._index_finger_position

    @property
    def thumb_finger_position(self) -> int:
        return self._thumb_finger_position

    def serialize(self) -> bytearray:
        raise NotImplementedError

    def deserialize(self, byte_array: bytearray):
        position_protobuf = SetPositions()
        position_protobuf.ParseFromString(byte_array)

        self._little_finger_position = position_protobuf.little_finger_position
        self._ring_finger_position = position_protobuf.ring_finger_position
        self._middle_finger_position = position_protobuf.middle_finger_position
        self._index_finger_position = position_protobuf.pointer_finger_position
        self._thumb_finger_position = position_protobuf.thumb_finger_position
