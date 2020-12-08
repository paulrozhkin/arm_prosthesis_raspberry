import datetime
import logging
from typing import List

from arm_prosthesis.external_communication.models.dto.gesture_dto import GestureDto


class GestureRepository:
    _logger = logging.getLogger('Main')

    def __init__(self, path_to_gesture_folder: str):
        pass

    def add_gesture(self, current_time: int, new_gesture: GestureDto):
        pass

    def remove_gesture(self, current_time: int, gesture_id: str):
        pass

    def get_gesture_by_id(self, gesture_id: str) -> GestureDto:
        pass

    def get_all_gestures(self) -> List[GestureDto]:
        pass
