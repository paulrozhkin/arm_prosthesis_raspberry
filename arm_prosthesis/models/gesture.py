from typing import List

from arm_prosthesis.models.gesture_action import GestureAction


class Gesture:
    def __init__(self, uuid: str, name: str, last_time_sync: int, iterable: bool, repetitions: int,
                 actions: List[GestureAction]):
        self._uuid = uuid
        self._name = name
        self._last_time_sync = last_time_sync
        self._iterable = iterable
        self._repetitions = repetitions
        self._actions = actions

    @property
    def uuid(self) -> str:
        return self._uuid

    @property
    def name(self) -> str:
        return self._name

    @property
    def last_time_sync(self) -> int:
        return self._last_time_sync

    @property
    def iterable(self) -> bool:
        return self._iterable

    @property
    def repetitions(self) -> int:
        return self._repetitions

    @property
    def actions(self) -> List[GestureAction]:
        return self._actions
