from configparser import ConfigParser


class Config:
    def __init__(self, log_to_file: bool, path_to_log: str):
        self._path_to_log = path_to_log
        self._log_to_file = log_to_file

    @property
    def path_to_log(self) -> str:
        return self._path_to_log

    @property
    def log_to_file(self) -> bool:
        return self._log_to_file


def load_config(path_to_config_ini: str) -> Config:
    config_parser = ConfigParser()
    config_parser.read(path_to_config_ini)

    config = Config(
        config_parser.getboolean('logger', 'log_to_file'),
        config_parser.get('logger', 'path_to_logs')
    )

    return config
