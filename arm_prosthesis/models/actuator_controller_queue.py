from enum import Enum

from arm_prosthesis.models.motor_positions import MotorPositions


class ActuatorControllerCommand(Enum):
    TELEMETRY = 0,
    SET_POSITIONS = 1


class ActuatorControllerQueue:

    def __init__(self, command_type: ActuatorControllerCommand, motor_position: MotorPositions = None):
        self._command_type = command_type

        if self._command_type == ActuatorControllerCommand.SET_POSITIONS and motor_position is None:
            raise Exception('Motor positions is None')

        self._motor_positions = motor_position

    @property
    def command_type(self) -> ActuatorControllerCommand:
        return self._command_type

    @property
    def motor_positions(self) -> MotorPositions:
        return self._motor_positions
