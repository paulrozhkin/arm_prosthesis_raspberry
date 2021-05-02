from arm_prosthesis.external_communication.models.dto.entity_dto import EntityDto
import enums_pb2 as enums
from telemetry_pb2 import Telemetry


class TelemetryDto(EntityDto):
    def __init__(self):
        self._emg_status: enums = enums.MODULE_STATUS_CONNECTION_ERROR
        self._display_status: enums = enums.MODULE_STATUS_CONNECTION_ERROR
        self._gyro_status: enums = enums.MODULE_STATUS_CONNECTION_ERROR
        self._driver_status: enums = enums.DRIVER_STATUS_CONNECTION_ERROR
        self._last_time_sync: int = 0
        self._emg: int = 0
        self._executable_gesture: str = ''
        self._power: int = 0
        self._index_finger_position: int = 0
        self._middle_finger_position: int = 0
        self._ring_finger_position: int = 0
        self._little_finger_position: int = 0
        self._thumb_finger_position: int = 0

    @property
    def emg_status(self) -> enums:
        return self._emg_status

    @emg_status.setter
    def emg_status(self, value: enums):
        self._emg_status = value

    @property
    def display_status(self) -> enums:
        return self._display_status

    @display_status.setter
    def display_status(self, value: enums):
        self._display_status = value

    @property
    def gyro_status(self) -> enums:
        return self._gyro_status

    @gyro_status.setter
    def gyro_status(self, value: enums):
        self._gyro_status = value

    @property
    def driver_status(self) -> enums:
        return self._driver_status

    @driver_status.setter
    def driver_status(self, value: enums):
        self._driver_status = value

    @property
    def last_time_sync(self) -> int:
        return self._last_time_sync

    @last_time_sync.setter
    def last_time_sync(self, value: int):
        self._last_time_sync = value

    @property
    def emg(self) -> int:
        return self._emg

    @emg.setter
    def emg(self, value: int):
        self._emg = value

    @property
    def executable_gesture(self) -> str:
        return self._executable_gesture

    @executable_gesture.setter
    def executable_gesture(self, value: str):
        self._executable_gesture = value

    @property
    def power(self) -> int:
        return self._power

    @power.setter
    def power(self, value: int):
        self._power = value

    @property
    def little_finger_position(self) -> int:
        return self._little_finger_position

    @little_finger_position.setter
    def little_finger_position(self, value: int):
        self._little_finger_position = value

    @property
    def ring_finger_position(self) -> int:
        return self._ring_finger_position

    @ring_finger_position.setter
    def ring_finger_position(self, value: int):
        self._ring_finger_position = value

    @property
    def middle_finger_position(self) -> int:
        return self._middle_finger_position

    @middle_finger_position.setter
    def middle_finger_position(self, value: int):
        self._middle_finger_position = value

    @property
    def index_finger_position(self) -> int:
        return self._index_finger_position

    @index_finger_position.setter
    def index_finger_position(self, value: int):
        self._index_finger_position = value

    @property
    def thumb_finger_position(self) -> int:
        return self._thumb_finger_position

    @thumb_finger_position.setter
    def thumb_finger_position(self, value: int):
        self._thumb_finger_position = value

    def serialize(self) -> bytes:
        telemetry_protobuf = self.convert_to_protobuf_gesture()
        return telemetry_protobuf.SerializeToString()

    def convert_to_protobuf_gesture(self) -> Telemetry:
        telemetry_protobuf = Telemetry()
        telemetry_protobuf.emg_status = self.emg_status
        telemetry_protobuf.display_status = self.display_status
        telemetry_protobuf.gyro_status = self.gyro_status
        telemetry_protobuf.driver_status = self.driver_status
        telemetry_protobuf.last_time_sync = self.last_time_sync
        telemetry_protobuf.emg = self.emg
        telemetry_protobuf.executable_gesture.value = self.executable_gesture
        telemetry_protobuf.power = self.power
        telemetry_protobuf.pointer_finger_position = self.index_finger_position
        telemetry_protobuf.middle_finger_position = self.middle_finger_position
        telemetry_protobuf.ring_finger_position = self.ring_finger_position
        telemetry_protobuf.little_finger_position = self.little_finger_position
        telemetry_protobuf.thumb_finger_position = self.thumb_finger_position

        return telemetry_protobuf

    def deserialize(self, byte_array: bytes):
        raise NotImplementedError()
