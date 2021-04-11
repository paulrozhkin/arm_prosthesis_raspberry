import json
import logging
import os
from typing import List, Dict

from arm_prosthesis.external_communication.models.dto.gesture_dto import GestureDto


class GestureRepository:
    _logger = logging.getLogger('Main')

    _gestures_dictionary: Dict[str, GestureDto]
    _path_to_gesture_folder: str
    _common_info_file_name = 'info.json'
    _gestures_directory_name = 'gestures'
    _gestures_file_extension = '.gesture'

    _common_info = {
        "last_time_sync": 0
    }

    def __init__(self, path_to_gesture_folder: str):

        if type(path_to_gesture_folder) is not str:
            self._logger.critical(f'Path to gestures incorrect. Is {path_to_gesture_folder}')
            raise Exception(f'Path to gestures incorrect. Is {path_to_gesture_folder}')

        self._path_to_gesture_folder = path_to_gesture_folder
        self._path_to_gestures = os.path.join(self._path_to_gesture_folder, self._gestures_directory_name)
        self._path_info_file = os.path.join(self._path_to_gesture_folder, self._common_info_file_name)

        self._gestures_dictionary = {}
        self._load_dictionary()

    def add_gesture(self, current_time: int, new_gesture: GestureDto):
        if new_gesture.id in self._gestures_dictionary:
            self._logger.info(f'Update gesture {new_gesture.id}')
        else:
            self._logger.info(f'Adding new gesture {new_gesture.id}')

        with open(os.path.join(self._path_to_gestures, new_gesture.id + self._gestures_file_extension),
                  'wb') as gesture_file:
            gesture_file.write(new_gesture.serialize())

        self._gestures_dictionary[new_gesture.id] = new_gesture
        self.update_time_sync(current_time)

    def remove_gesture(self, current_time: int, gesture_id: str):
        self._logger.info(f'Remove gesture {gesture_id}')
        os.remove(os.path.join(self._path_to_gestures, gesture_id + self._gestures_file_extension))

        del self._gestures_dictionary[gesture_id]
        self.update_time_sync(current_time)

    def get_gesture_by_id(self, gesture_id: str) -> GestureDto:
        self._logger.info(f'Get gesture {gesture_id}')
        return self._gestures_dictionary[gesture_id]

    def get_all_gestures(self) -> List[GestureDto]:
        self._logger.info(f'Get all gestures')
        return list(self._gestures_dictionary.values())

    @property
    def last_time_sync(self) -> int:
        return self._common_info['last_time_sync']

    def update_time_sync(self, new_time_sync):
        self._logger.info(f'Update last time sync to new value: {new_time_sync}')

        self._common_info['last_time_sync'] = new_time_sync

        with open(self._path_info_file, 'w') as info:
            json.dump(self._common_info, info)

    def _load_dictionary(self):
        self._logger.info(f'Load gestures')

        if os.path.isdir(self._path_to_gestures) is False:
            self._create_default()

        with open(self._path_info_file, 'r') as info:
            self._common_info = json.load(info)

        self._logger.info(f'Loaded time sync: {self._common_info["last_time_sync"]}')

        for file in os.listdir(self._path_to_gestures):
            if file.endswith(self._gestures_file_extension):
                with open(os.path.join(self._path_to_gestures, file), 'rb') as gesture_file:
                    gesture_dto = GestureDto()
                    gesture_dto.deserialize(gesture_file.read())
                    self._gestures_dictionary[gesture_dto.id] = gesture_dto

        self._logger.info(f'Loaded gestures count: {len(self._gestures_dictionary)}')

    def _create_default(self):
        self._logger.info('Start create new gestures directory')
        os.makedirs(self._path_to_gestures)

        self.update_time_sync(0)
