import logging
import os
from typing import Dict, List

import uuid

from arm_prosthesis.external_communication.models.dto.mio_pattern_dto import MioPatternDto
from arm_prosthesis.external_communication.models.dto.set_mio_patterns_dto import SetMioPatternsDto


class MioPatternsService:
    _logger = logging.getLogger('Main')
    _patterns_dictionary: Dict[int, MioPatternDto]

    _default_patterns = [0, 1]

    def __init__(self, path_to_patterns_file: str):
        if type(path_to_patterns_file) is not str:
            self._logger.critical(f'Path to patterns incorrect. Is {path_to_patterns_file}')
            raise Exception(f'Path to patterns incorrect. Is {path_to_patterns_file}')

        self._path_to_patterns_file = path_to_patterns_file
        self._patterns_dictionary = {}
        self._load_patterns()

    def get_mio_patterns(self) -> List[MioPatternDto]:
        return list(self._patterns_dictionary.values())

    def get_gesture_id_by_pattern(self, pattern: int) -> str:
        self._logger.info(f'Get pattern {pattern}')
        return self._patterns_dictionary[pattern].gesture_id

    def update_mio_patterns(self, patterns: List[MioPatternDto]):
        set_mio_patterns_dto = SetMioPatternsDto()
        set_mio_patterns_dto.patterns_dto = patterns

        for update_pattern in patterns:
            if update_pattern.pattern not in self._default_patterns:
                raise Exception(f'Unknown pattern: {update_pattern.pattern}')

            if self._is_valid_uuid(update_pattern.gesture_id) is False:
                raise Exception(f'Incorrect gesture id: {update_pattern.gesture_id}')

            self._patterns_dictionary[update_pattern.pattern] = update_pattern

        with open(os.path.join(self._path_to_patterns_file),
                  'wb') as patterns_file:
            patterns_file.write(set_mio_patterns_dto.serialize())

    def _load_patterns(self):
        self._logger.info(f'Load patterns')

        if os.path.isfile(self._path_to_patterns_file) is False:
            self._create_default()

        with open(self._path_to_patterns_file, 'rb') as mio_patterns_file:
            set_mio_patterns_dto = SetMioPatternsDto()
            set_mio_patterns_dto.deserialize(mio_patterns_file.read())

            for pattern in set_mio_patterns_dto.patterns_dto:
                self._patterns_dictionary[pattern.pattern] = pattern

        self._logger.info(f'Loaded patterns count: {len(self._patterns_dictionary)}')

    def _create_default(self):
        self._logger.info('Start create new patterns directory')

        patterns = []
        for default_pattern_id in self._default_patterns:
            pattern = MioPatternDto()
            pattern.pattern = default_pattern_id
            pattern.gesture_id = '00000000-0000-0000-0000-000000000000'
            patterns.append(pattern)

        self.update_mio_patterns(patterns)

    @staticmethod
    def _is_valid_uuid(val):
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False
