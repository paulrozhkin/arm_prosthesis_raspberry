import json

from arm_prosthesis.external_communication.models.dto.entity_dto import EntityDto
from arm_prosthesis.external_communication.services.dto_to_entity_converter import DtoToEntityConverter
from settings_pb2 import GetSettings


class GetSettingsDto(EntityDto):
    def __init__(self):
        self._enable_emg: bool = False
        self._enable_display: bool = False
        self._enable_gyro: bool = False
        self._enable_driver: bool = False

    @property
    def enable_emg(self) -> bool:
        return self._enable_emg

    @enable_emg.setter
    def enable_emg(self, value: bool):
        self._enable_emg = value

    @property
    def enable_display(self) -> bool:
        return self._enable_display

    @enable_display.setter
    def enable_display(self, value: bool):
        self._enable_display = value

    @property
    def enable_gyro(self) -> bool:
        return self._enable_gyro

    @enable_gyro.setter
    def enable_gyro(self, value: bool):
        self._enable_gyro = value

    @property
    def enable_driver(self) -> bool:
        return self._enable_driver

    @enable_driver.setter
    def enable_driver(self, value: bool):
        self._enable_driver = value

    def deserialize(self, byte_array: bytes):
        get_settings_protobuf = GetSettings()
        get_settings_protobuf.ParseFromString(byte_array)
        self._enable_emg = get_settings_protobuf.enable_emg
        self._enable_display = get_settings_protobuf.enable_display
        self._enable_gyro = get_settings_protobuf.enable_gyro
        self._enable_driver = get_settings_protobuf.enable_driver

    def serialize(self) -> bytes:
        get_settings_protobuf = GetSettings()
        get_settings_protobuf.enable_emg = self._enable_emg
        get_settings_protobuf.enable_display = self._enable_display
        get_settings_protobuf.enable_gyro = self._enable_gyro
        get_settings_protobuf.enable_driver = self._enable_driver
        return get_settings_protobuf.SerializeToString()

    def __str__(self):
        return json.dumps(self.__dict__, indent=2)
