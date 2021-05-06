from arm_prosthesis.external_communication.models.dto.entity_dto import EntityDto
from arm_prosthesis.external_communication.services.dto_to_entity_converter import DtoToEntityConverter
from settings_pb2 import SetSettings


class SetSettingsDto(EntityDto):
    def __init__(self):
        self._enable_emg: bool = False
        self._enable_display: bool = False
        self._enable_gyro: bool = False
        self._enable_driver: bool = False
        self._power_off: bool = False

    @property
    def enable_emg(self) -> bool:
        return self._enable_emg

    @property
    def enable_display(self) -> bool:
        return self._enable_display

    @property
    def enable_gyro(self) -> bool:
        return self._enable_gyro

    @property
    def enable_driver(self) -> bool:
        return self._enable_driver

    @property
    def power_off(self) -> bool:
        return self._power_off

    def deserialize(self, byte_array: bytes):
        set_settings_protobuf = SetSettings()
        set_settings_protobuf.ParseFromString(byte_array)
        self._enable_emg = set_settings_protobuf.enable_emg
        self._enable_display = set_settings_protobuf.enable_display
        self._enable_gyro = set_settings_protobuf.enable_gyro
        self._enable_driver = set_settings_protobuf.enable_driver
        self._power_off = set_settings_protobuf.power_off

    def serialize(self) -> bytes:
        raise NotImplementedError()
