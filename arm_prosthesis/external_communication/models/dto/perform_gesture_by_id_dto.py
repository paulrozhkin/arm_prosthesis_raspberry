from arm_prosthesis.external_communication.models.dto.entity_dto import EntityDto
from gestures_pb2 import SetPositions, PerformGestureById


class PerformGestureByIdDto(EntityDto):

    def __init__(self):
        self._id = ''

    @property
    def id(self) -> str:
        return self._id

    def serialize(self) -> bytearray:
        raise NotImplementedError

    def deserialize(self, byte_array: bytes):
        perform_by_id_protobuf = PerformGestureById()
        perform_by_id_protobuf.ParseFromString(byte_array)

        self._id = perform_by_id_protobuf.id.value
