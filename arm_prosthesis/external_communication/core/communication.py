import logging
import os
import time
import traceback
from queue import Queue

from arm_prosthesis.config.configuration import Config
from arm_prosthesis.external_communication.core.connectors.mqtt_connector import MqttConnector
from arm_prosthesis.external_communication.core.connectors.rfcc_connector import RFCCConnector
from arm_prosthesis.external_communication.models.command_type import CommandType
from arm_prosthesis.external_communication.models.dto.delete_gesture_dto import DeleteGestureDto
from arm_prosthesis.external_communication.models.dto.get_gestures_dto import GetGesturesDto
from arm_prosthesis.external_communication.models.dto.get_settings_dto import GetSettingsDto
from arm_prosthesis.external_communication.models.dto.get_telemetry_dto import GetTelemetryDto
from arm_prosthesis.external_communication.models.dto.perform_gesture_by_id_dto import PerformGestureByIdDto
from arm_prosthesis.external_communication.models.dto.perform_gesture_by_raw_dto import PerformGestureRawDto
from arm_prosthesis.external_communication.models.dto.save_gesture_dto import SaveGestureDto
from arm_prosthesis.external_communication.models.dto.set_positions_dto import SetPositionsDto
from arm_prosthesis.external_communication.models.dto.set_settings_dto import SetSettingsDto
from arm_prosthesis.external_communication.models.dto.start_telemetry_dto import StartTelemetryDto
from arm_prosthesis.external_communication.models.dto.update_last_time_sync_dto import UpdateLastTimeSyncDto
from arm_prosthesis.external_communication.models.request import Request
from arm_prosthesis.external_communication.models.response import Response
from arm_prosthesis.external_communication.services.dto_to_entity_converter import DtoToEntityConverter
from arm_prosthesis.services.motor_driver_communication import ActuatorControllerService
from arm_prosthesis.services.myoelectronics_service import MyoelectronicsService
from arm_prosthesis.utils.stoppable_thread import StoppableThread
from arm_prosthesis.external_communication.services.telemetry_service import TelemetryService
from arm_prosthesis.hand_controller import HandController
from arm_prosthesis.models.positions import Positions
from arm_prosthesis.services.gesture_repository import GestureRepository
from arm_prosthesis.services.settings_dao import SettingsDao
from errors_pb2 import Error


class Communication:
    _logger = logging.getLogger('Main')
    _settings: GetSettingsDto
    _telemetry_thread: StoppableThread = None
    _mqtt_connector: MqttConnector = None
    _rfcc_connector: RFCCConnector = None
    _interval_100_hz_in_ms = 10
    _interval_2_days_in_ms = 172800000

    def __init__(self, hand_controller: HandController,
                 config: Config,
                 gesture_repository: GestureRepository,
                 telemetry_service: TelemetryService,
                 settings_dao: SettingsDao,
                 myoelectronics_service: MyoelectronicsService,
                 driver_communication: ActuatorControllerService):
        self._gesture_repository = gesture_repository
        self._settings_dao = settings_dao
        self._hand_controller = hand_controller
        self._config = config
        self._telemetry_service = telemetry_service
        self._myoelectronics_service = myoelectronics_service
        self._driver_communication = driver_communication
        self._settings = self._settings_dao.get()

        self._request_queue: 'Queue[Request]' = Queue()

        if self._config.mqtt_enabled:
            self._mqtt_connector = MqttConnector(self._config, self.request_queue)

        if self._config.rfcomm_enabled:
            self._rfcc_connector = RFCCConnector(self._config, self.request_queue)

        self._logger.info('Communication initialized')

    @property
    def request_queue(self) -> 'Queue[Request]':
        return self._request_queue

    def _send_telemetry(self):
        if (self._mqtt_connector and self._mqtt_connector.connected) \
                or (self._rfcc_connector and self._rfcc_connector.connected):

            telemetry = self._telemetry_service.get_telemetry()
            telemetry_response = Response(CommandType.Telemetry, telemetry.serialize())

            if self._mqtt_connector and self._mqtt_connector.connected:
                self._mqtt_connector.write_response(telemetry_response)

            if self._rfcc_connector and self._rfcc_connector.connected:
                self._rfcc_connector.write_response(telemetry_response)

    def run(self):
        self._logger.info('Communication running')

        if self._mqtt_connector:
            self._mqtt_connector.start()

        if self._rfcc_connector:
            self._rfcc_connector.start()

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

            if request.command_type == CommandType.UpdateLastTimeSync:
                self.handle_update_last_time_sync(request.payload)
                request.response_writer.write_response(Response(CommandType.Ok, None))
                return

            if request.command_type == CommandType.GetTelemetry:
                get_telemetry_dto = self.handle_get_telemetry()
                request.response_writer.write_response(
                    Response(CommandType.GetTelemetry, get_telemetry_dto.serialize()))
                return

            if request.command_type == CommandType.StartTelemetry:
                self.handle_start_telemetry(request.payload)
                request.response_writer.write_response(Response(CommandType.Ok, None))
                return

            if request.command_type == CommandType.StopTelemetry:
                self.handle_stop_telemetry()
                request.response_writer.write_response(Response(CommandType.Ok, None))
                return

            if request.command_type == CommandType.GetMioPatterns:
                raise NotImplementedError

            if request.command_type == CommandType.SetMioPatterns:
                raise NotImplementedError

            raise Exception(f'Command {request.command_type} not supporting')
        except:
            e = traceback.format_exc()
            logging.error(f'Error request handling: {e}')
            error = Error()
            error.message = e
            error_response = Response(CommandType.Error, error.SerializeToString())
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

    def handle_update_last_time_sync(self, payload: bytes):
        logging.info(f'Start handling update last time sync')

        update_last_time_sync_dto = UpdateLastTimeSyncDto()
        update_last_time_sync_dto.deserialize(payload)
        self._gesture_repository.update_time_sync(update_last_time_sync_dto.last_time_sync)

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

        self._settings_dao.save(settings_dto)

        if settings_dto.power_off:
            logging.info(f'Power off')
            os.system("shutdown now -h")
            exit()

        old_emg = self._settings.enable_emg

        self._settings = self._settings_dao.get()

        if self._settings.enable_emg != old_emg:
            if self._settings.enable_emg:
                self._myoelectronics_service.start()
            else:
                self._myoelectronics_service.stop()

    def handle_start_telemetry(self, payload):
        if self._telemetry_thread is not None:
            raise Exception('Telemetry already started')

        start_telemetry_dto = StartTelemetryDto()
        start_telemetry_dto.deserialize(payload)

        if start_telemetry_dto.interval_ms < self._interval_100_hz_in_ms \
                or start_telemetry_dto.interval_ms > self._interval_2_days_in_ms:
            raise Exception('Incorrect interval')

        interval_in_seconds = start_telemetry_dto.interval_ms / 1000

        self._driver_communication.enable_telemetry()
        self._telemetry_thread = StoppableThread(target=self._send_telemetry, timeout=interval_in_seconds)
        self._telemetry_thread.start()

    def handle_get_telemetry(self) -> GetTelemetryDto:
        get_telemetry_dto = GetTelemetryDto()
        telemetry = self._telemetry_service.get_telemetry()
        get_telemetry_dto.telemetry = telemetry
        return get_telemetry_dto

    def handle_stop_telemetry(self):
        if self._telemetry_thread is None:
            raise Exception('Telemetry not started')

        self._driver_communication.disable_telemetry()
        self._telemetry_thread.stop()
        self._telemetry_thread = None
