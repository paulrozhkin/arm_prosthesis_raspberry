from arm_prosthesis.external_communication.models.dto.entity_dto import EntityDto


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
        raise NotImplementedError
