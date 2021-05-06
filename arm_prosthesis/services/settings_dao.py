import json
import logging
import os

from arm_prosthesis.external_communication.models.dto.get_settings_dto import GetSettingsDto
from arm_prosthesis.external_communication.models.dto.set_settings_dto import SetSettingsDto


class SettingsDao:
    _logger = logging.getLogger('Main')

    _settings: GetSettingsDto

    def __init__(self, path_to_settings_file: str):
        if type(path_to_settings_file) is not str:
            self._logger.critical(f'Path to settings incorrect. Is {path_to_settings_file}')
            raise Exception(f'Path to settings incorrect. Is {path_to_settings_file}')

        self._path_to_settings_file = path_to_settings_file
        self._settings = self._load_settings()

    def get(self) -> GetSettingsDto:
        return self._settings

    def save(self, settings: SetSettingsDto):
        self._settings.enable_emg = settings.enable_emg
        self._settings.enable_display = settings.enable_display
        self._settings.enable_driver = settings.enable_driver
        self._settings.enable_gyro = settings.enable_gyro

        self._save_settings_to_file(self._settings)

    def _load_settings(self) -> GetSettingsDto:
        self._logger.info(f'Load settings')

        if os.path.isfile(self._path_to_settings_file) is False:
            self._create_default()

        return self._load_settings_from_file()

    def _create_default(self):
        self._logger.info('Start create new settings')

        settings = GetSettingsDto()
        settings.enable_emg = False
        settings.enable_driver = False
        settings.enable_display = False
        settings.enable_gyro = False

        self._save_settings_to_file(settings)

    def _save_settings_to_file(self, settings: GetSettingsDto):
        settings_content_default = {
            "enable_emg": settings.enable_emg,
            "enable_display": settings.enable_display,
            "enable_gyro": settings.enable_gyro,
            "enable_driver": settings.enable_driver
        }

        with open(self._path_to_settings_file, 'w') as settings_file:
            json.dump(settings_content_default, settings_file)

    def _load_settings_from_file(self) -> GetSettingsDto:
        settings = GetSettingsDto()

        with open(self._path_to_settings_file, 'r') as settings_file:
            settings_content = json.load(settings_file)
            settings.enable_emg = settings_content['enable_emg']
            settings.enable_display = settings_content['enable_display']
            settings.enable_gyro = settings_content['enable_gyro']
            settings.enable_driver = settings_content['enable_driver']

        return settings
