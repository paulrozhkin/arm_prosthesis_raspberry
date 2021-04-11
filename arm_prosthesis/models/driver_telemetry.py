from arm_prosthesis.models.motor_positions import MotorPositions
from enums_pb2 import DriverStatusType


class DriverTelemetry(MotorPositions):
    def __init__(self, driver_status: DriverStatusType, little_finger_angle_position, ring_finger_angle_position,
                 middle_finger_angle_position,
                 index_finger_angle_position, thumb_finger_angle_position, thumb_ejector_angle_position):
        super().__init__(little_finger_angle_position, ring_finger_angle_position, middle_finger_angle_position,
                         index_finger_angle_position, thumb_finger_angle_position, thumb_ejector_angle_position)

        self._driver_status = driver_status

    @property
    def driver_status(self) -> DriverStatusType:
        return self._driver_status
