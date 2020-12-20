from arm_prosthesis.external_communication.models.dto.gesture_action_dto import GestureActionDto
from arm_prosthesis.external_communication.models.dto.gesture_dto import GestureDto
from arm_prosthesis.models.gesture import Gesture
from arm_prosthesis.models.gesture_action import GestureAction
from arm_prosthesis.models.mode_type import ModeType
import enums_pb2 as enums


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

    @staticmethod
    def convert_mode_type_protobuf_to_mode_type(protobuf: enums) -> ModeType:
        if protobuf == enums.MODE_AUTO:
            return ModeType.Auto
        else:
            if protobuf == enums.MODE_COMMANDS:
                return ModeType.Commands
            else:
                if protobuf == enums.MODE_MIO:
                    return ModeType.MIO
                else:
                    raise Exception(f'Can not convert {protobuf} to ModeType')

    @staticmethod
    def convert_mode_type_to_mode_type_protobuf(value: ModeType) -> enums:
        if value == ModeType.Auto:
            return enums.MODE_AUTO
        else:
            if value == ModeType.Commands:
                return enums.MODE_COMMANDS
            else:
                if value == ModeType.MIO:
                    return enums.MODE_MIO
                else:
                    raise Exception(f'Can not convert {value} to protobuf enum')
