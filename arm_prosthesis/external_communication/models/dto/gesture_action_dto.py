from arm_prosthesis.external_communication.models.dto.entity_dto import EntityDto
from gestures_pb2 import GestureAction


class GestureActionDto(EntityDto):
    def __init__(self):
        self._little_finger_position = 0
        self._ring_finger_position = 0
        self._middle_finger_position = 0
        self._index_finger_position = 0
        self._thumb_finger_position = 0
        self._delay = 0

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

    @property
    def delay(self) -> int:
        return self._delay

    def create_from_protobuf_action(self, action_proto: GestureAction):
        self._little_finger_position = action_proto.little_finger_position
        self._ring_finger_position = action_proto.ring_finger_position
        self._middle_finger_position = action_proto.middle_finger_position
        self._index_finger_position = action_proto.pointer_finger_position
        self._thumb_finger_position = action_proto.thumb_finger_position
        self._delay = action_proto.delay

    def convert_to_protobuf_action(self) -> GestureAction:
        action_proto = GestureAction()
        action_proto.little_finger_position = self.little_finger_position
        action_proto.ring_finger_position = self.ring_finger_position
        action_proto.middle_finger_position = self.middle_finger_position
        action_proto.pointer_finger_position = self.index_finger_position
        action_proto.thumb_finger_position = self.thumb_finger_position
        action_proto.delay = self._delay
        return action_proto

    def serialize(self) -> bytes:
        raise NotImplementedError

    def deserialize(self, byte_array: bytes):
        raise NotImplementedError
