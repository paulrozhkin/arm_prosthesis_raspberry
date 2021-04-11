from arm_prosthesis.external_communication.models.dto.entity_dto import EntityDto
from gestures_pb2 import UpdateLastTimeSync


class UpdateLastTimeSyncDto(EntityDto):

    def __init__(self):
        self._last_time_sync = 0

    @property
    def last_time_sync(self) -> int:
        return self._last_time_sync

    def serialize(self) -> bytes:
        raise NotImplementedError

    def deserialize(self, byte_array: bytes):
        update_last_time_sync_protobuf = UpdateLastTimeSync()
        update_last_time_sync_protobuf.ParseFromString(byte_array)

        self._last_time_sync = update_last_time_sync_protobuf.last_time_sync
