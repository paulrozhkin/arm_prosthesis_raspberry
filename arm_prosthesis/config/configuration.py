import json
from configparser import ConfigParser


class Config:
    def __init__(self, log_to_file: bool, path_to_log: str, mqtt_enabled: bool, mqtt_address: str,
                 rfcomm_enabled: bool, gestures_path: str, settings_path: str, patterns_path: str,
                 model_path: str):
        self._path_to_log = path_to_log
        self._log_to_file = log_to_file
        self._mqtt_enabled = mqtt_enabled
        self._mqtt_address = mqtt_address
        self._rfcomm_enabled = rfcomm_enabled
        self._gestures_path = gestures_path
        self._settings_path = settings_path
        self._patterns_path = patterns_path
        self._model_path = model_path

    @property
    def path_to_log(self) -> str:
        return self._path_to_log

    @property
    def log_to_file(self) -> bool:
        return self._log_to_file

    @property
    def mqtt_enabled(self) -> bool:
        return self._mqtt_enabled

    @property
    def mqtt_address(self) -> str:
        return self._mqtt_address

    @property
    def rfcomm_enabled(self) -> bool:
        return self._rfcomm_enabled

    @property
    def gestures_path(self) -> str:
        return self._gestures_path

    @property
    def settings_path(self) -> str:
        return self._settings_path

    @property
    def patterns_path(self) -> str:
        return self._patterns_path

    @property
    def model_path(self) -> str:
        return self._model_path

    def __str__(self):
        return json.dumps(self.__dict__, indent=2)


def load_config(path_to_config_ini: str) -> Config:
    config_parser = ConfigParser()
    config_parser.read(path_to_config_ini)

    mqtt_enabled = config_parser.getboolean('mqtt_proxy', 'mqtt_enabled')
    mqtt_address = config_parser.get('mqtt_proxy', 'mqtt_address') if mqtt_enabled else None

    config = Config(
        config_parser.getboolean('logger', 'log_to_file'),
        config_parser.get('logger', 'path_to_logs'),
        mqtt_enabled,
        mqtt_address,
        config_parser.getboolean('rfcomm', 'rfcomm_enabled'),
        config_parser.get('gestures', 'gestures_path'),
        config_parser.get('settings', 'settings_path'),
        config_parser.get('patterns', 'patterns_path'),
        config_parser.get('patterns', 'model_path')
    )

    return config
