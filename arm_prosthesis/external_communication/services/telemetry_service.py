from arm_prosthesis.external_communication.models.dto.telemetry_dto import TelemetryDto
from arm_prosthesis.services.gesture_repository import GestureRepository
from arm_prosthesis.services.motor_driver_communication import ActuatorControllerService
import enums_pb2 as enums


class TelemetryService:
    _gesture_repository: GestureRepository
    _driver_communication: ActuatorControllerService

    def __init__(self, gesture_repository: GestureRepository,
                 driver_communication: ActuatorControllerService):
        self._gesture_repository = gesture_repository
        self._driver_communication = driver_communication

    def get_telemetry(self) -> TelemetryDto:
        telemetry = TelemetryDto()
        telemetry.last_time_sync = self._gesture_repository.last_time_sync

        driver_telemetry = self._driver_communication.telemetry

        telemetry.driver_status = driver_telemetry.driver_status
        if telemetry.driver_status != enums.DRIVER_STATUS_CONNECTION_ERROR:
            telemetry.little_finger_position = driver_telemetry.little_finger_angle_position
            telemetry.ring_finger_position = driver_telemetry.ring_finger_angle_position
            telemetry.middle_finger_position = driver_telemetry.middle_finger_angle_position
            telemetry.index_finger_position = driver_telemetry.index_finger_angle_position
            telemetry.thumb_finger_position = driver_telemetry.thumb_finger_angle_position

        return telemetry
