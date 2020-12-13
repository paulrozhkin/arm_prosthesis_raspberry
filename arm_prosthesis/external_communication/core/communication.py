import logging
import threading
import time
import traceback
from queue import Queue

from arm_prosthesis.config.configuration import Config
from arm_prosthesis.external_communication.core.connectors.mqtt_connector import MqttConnector
from arm_prosthesis.external_communication.models.command_type import CommandType
from arm_prosthesis.external_communication.models.dto.delete_gesture_dto import DeleteGestureDto
from arm_prosthesis.external_communication.models.dto.get_gestures_dto import GetGesturesDto
from arm_prosthesis.external_communication.models.dto.get_settings_dto import GetSettingsDto
from arm_prosthesis.external_communication.models.dto.perform_gesture_by_id_dto import PerformGestureByIdDto
from arm_prosthesis.external_communication.models.dto.perform_gesture_by_raw_dto import PerformGestureRawDto
from arm_prosthesis.external_communication.models.dto.save_gesture_dto import SaveGestureDto
from arm_prosthesis.external_communication.models.dto.set_positions_dto import SetPositionsDto
from arm_prosthesis.external_communication.models.dto.set_settings_dto import SetSettingsDto
from arm_prosthesis.external_communication.models.request import Request
from arm_prosthesis.external_communication.models.response import Response
from arm_prosthesis.external_communication.services.dto_to_entity_converter import DtoToEntityConverter
from arm_prosthesis.external_communication.services.telemetry_service import TelemetryService
from arm_prosthesis.hand_controller import HandController
from arm_prosthesis.models.positions import Positions
from arm_prosthesis.services.gesture_repository import GestureRepository
from arm_prosthesis.services.settings_dao import SettingsDao


class Communication:
    _logger = logging.getLogger('Main')
    _default_telemetry_period = 1.0
    _settings: GetSettingsDto

    def __init__(self, hand_controller: HandController, config: Config, gesture_repository: GestureRepository,
                 telemetry_service: TelemetryService, settings_dao: SettingsDao):
        self._gesture_repository = gesture_repository
        self._settings_dao = settings_dao
        self._hand_controller = hand_controller
        self._config = config
        self._telemetry_service = telemetry_service
        self._settings = self._settings_dao.get()

        self._telemetry_period = self._default_telemetry_period
        self._telemetry_thread = threading.Thread(target=self._send_telemetry)

        self._request_queue: 'Queue[Request]' = Queue()

        if self._config.mqtt_enabled:
            self._mqtt_connector = MqttConnector(self._config, self.request_queue)

        if self._config.rfcomm_enabled:
            raise NotImplementedError

        self._logger.info('Communication initialized')

    @property
    def request_queue(self) -> 'Queue[Request]':
        return self._request_queue

    def _send_telemetry(self):
        while 1:
            if self._mqtt_connector and self._mqtt_connector.connected:
                telemetry = self._telemetry_service.get_telemetry()
                telemetry.telemetry_frequency = int(1/self._telemetry_period)
                telemetry_response = Response(CommandType.Telemetry, telemetry.serialize())
                self._mqtt_connector.write_response(telemetry_response)
            time.sleep(self._telemetry_period)

    def run(self):
        self._logger.info('Communication running')

        if self._mqtt_connector:
            self._mqtt_connector.start()

        self._telemetry_thread.start()

        while 1:
            self._logger.info('Wait new request')
            request = self._request_queue.get()
            self._logger.info('New request receive from the queue. Start handle request')
            self.handle_request(request)

    def handle_request(self, request: Request):
        try:
            logging.info(f'Request {request.command_type}')
            if request.command_type == CommandType.SetPositions:
                self.handle_set_positions_request(request.payload)
                request.response_writer.write_response(Response(CommandType.Ok, None))
                return

            if request.command_type == CommandType.SaveGesture:
                self.handle_save_gesture(request.payload)
                request.response_writer.write_response(Response(CommandType.Ok, None))
                return

            if request.command_type == CommandType.DeleteGesture:
                self.handle_delete_gesture(request.payload)
                request.response_writer.write_response(Response(CommandType.Ok, None))
                return

            if request.command_type == CommandType.PerformGestureId:
                self.handle_perform_gesture_by_id(request.payload)
                request.response_writer.write_response(Response(CommandType.Ok, None))
                return

            if request.command_type == CommandType.PerformGestureRaw:
                self.handle_perform_gesture_raw(request.payload)
                request.response_writer.write_response(Response(CommandType.Ok, None))
                return

            if request.command_type == CommandType.GetGestures:
                gestures_dto = self.handle_get_gesture()
                request.response_writer.write_response(Response(CommandType.GetGestures, gestures_dto.serialize()))
                return

            if request.command_type == CommandType.GetSettings:
                settings_dto = self.handle_get_settings()
                request.response_writer.write_response(Response(CommandType.GetSettings, settings_dto.serialize()))
                return

            if request.command_type == CommandType.SetSettings:
                self.handle_set_settings(request.payload)
                request.response_writer.write_response(Response(CommandType.Ok, None))
                return

            raise Exception(f'Command {request.command_type} not supporting')
        except:
            e = traceback.format_exc()
            logging.error(f'Error request handling: {e}')
            error_response = Response(CommandType.Error)
            request.response_writer.write_response(error_response)

    def handle_set_positions_request(self, payload: bytes):
        logging.info(f'Start handling set positions')
        set_position = SetPositionsDto()
        set_position.deserialize(payload)
        positions = Positions(set_position.little_finger_position, set_position.ring_finger_position,
                              set_position.middle_finger_position, set_position.index_finger_position,
                              set_position.thumb_finger_position)
        self._hand_controller.set_positions(positions)

    def handle_save_gesture(self, payload: bytes):
        logging.info(f'Start handling save gesture')
        save_gesture_dto = SaveGestureDto()
        save_gesture_dto.deserialize(payload)

        self._gesture_repository.add_gesture(save_gesture_dto.time_sync, save_gesture_dto.gesture_dto)

    def handle_delete_gesture(self, payload: bytes):
        logging.info(f'Start handling delete gesture')

        delete_gesture_dto = DeleteGestureDto()
        delete_gesture_dto.deserialize(payload)

        self._gesture_repository.remove_gesture(delete_gesture_dto.time_sync, delete_gesture_dto.id)

    def handle_perform_gesture_by_id(self, payload: bytes):
        logging.info(f'Start handling perform gesture by id')

        perform_gesture_by_id_dto = PerformGestureByIdDto()
        perform_gesture_by_id_dto.deserialize(payload)

        gesture = self._gesture_repository.get_gesture_by_id(perform_gesture_by_id_dto.id)

        self._hand_controller.perform_gesture(DtoToEntityConverter.convert_gesture_dto_to_gesture(gesture))

    def handle_perform_gesture_raw(self, payload: bytes):
        logging.info(f'Start handling perform gesture raw')

        perform_gesture_raw_dto = PerformGestureRawDto()
        perform_gesture_raw_dto.deserialize(payload)

        self._hand_controller.perform_gesture(
            DtoToEntityConverter.convert_gesture_dto_to_gesture(perform_gesture_raw_dto.gesture_dto))

    def handle_get_gesture(self) -> GetGesturesDto:
        logging.info(f'Start handling get gesture')

        get_gestures_dto = GetGesturesDto()
        get_gestures_dto.last_time_sync = self._gesture_repository.last_time_sync
        get_gestures_dto.gestures_dto = self._gesture_repository.get_all_gestures()
        return get_gestures_dto

    def handle_get_settings(self) -> GetSettingsDto:
        logging.info(f'Start handling get settings')

        current_settings = self._settings_dao.get()
        return current_settings

    def handle_set_settings(self, payload: bytes):
        logging.info(f'Start handling set settings')

        settings_dto = SetSettingsDto()
        settings_dto.deserialize(payload)

        if settings_dto.telemetry_frequency <= 1:
            self._telemetry_period = 1.0
        else:
            if settings_dto.telemetry_frequency >= 20:
                self._telemetry_period = 0.05
            else:
                self._telemetry_period = 1 / settings_dto.telemetry_frequency

        self._settings_dao.save(settings_dto)
        self._settings = self._settings_dao.get()