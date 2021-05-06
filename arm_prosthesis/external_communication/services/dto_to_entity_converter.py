from arm_prosthesis.external_communication.models.dto.gesture_action_dto import GestureActionDto
from arm_prosthesis.external_communication.models.dto.gesture_dto import GestureDto
from arm_prosthesis.models.gesture import Gesture
from arm_prosthesis.models.gesture_action import GestureAction


class DtoToEntityConverter:
    @staticmethod
    def convert_gesture_dto_to_gesture(gesture_dto: GestureDto) -> Gesture:
        actions = []
        for action_dto in gesture_dto.actions:
            actions.append(DtoToEntityConverter.convert_action_dto_to_action(action_dto))

        return Gesture(gesture_dto.id, gesture_dto.name, gesture_dto.last_time_sync, gesture_dto.iterable,
                       gesture_dto.repetitions,
                       actions)

    @staticmethod
    def convert_action_dto_to_action(action_dto: GestureActionDto) -> GestureAction:
        return GestureAction(action_dto.little_finger_position, action_dto.ring_finger_position,
                             action_dto.middle_finger_position, action_dto.index_finger_position,
                             action_dto.thumb_finger_position, 0, action_dto.delay)
