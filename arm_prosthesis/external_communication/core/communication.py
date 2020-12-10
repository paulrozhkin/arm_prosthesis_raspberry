import logging
import sys
import traceback
from queue import Queue

from arm_prosthesis.config.configuration import Config
from arm_prosthesis.external_communication.core.connectors.mqtt_connector import MqttConnector
from arm_prosthesis.external_communication.models.command_type import CommandType
from arm_prosthesis.external_communication.models.dto.delete_gesture_dto import DeleteGestureDto
from arm_prosthesis.external_communication.models.dto.perform_gesture_by_id_dto import PerformGestureByIdDto
from arm_prosthesis.external_communication.models.dto.perform_gesture_by_raw_dto import PerformGestureRawDto
from arm_prosthesis.external_communication.models.dto.save_gesture_dto import SaveGestureDto
from arm_prosthesis.external_communication.models.dto.set_positions_dto import SetPositionsDto
from arm_prosthesis.external_communication.models.request import Request
from arm_prosthesis.external_communication.models.response import Response
from arm_prosthesis.external_communication.services.dto_to_entity_converter import DtoToEntityConverter
from arm_prosthesis.hand_controller import HandController
from arm_prosthesis.models.positions import Positions
from arm_prosthesis.services.gesture_repository import GestureRepository


class Communication:
    _logger = logging.getLogger('Main')

    def __init__(self, hand_controller: HandController, config: Config, gesture_repository: GestureRepository):
        self._gesture_repository = gesture_repository
        self._hand_controller = hand_controller
        self._config = config

        self._request_queue: 'Queue[Request]' = Queue()

        if self._config.mqtt_enabled:
            self._mqtt_connector = MqttConnector(self._config, self.request_queue)

        if self._config.rfcomm_enabled:
            raise NotImplementedError

        self._logger.info('Communication initialized')

    @property
    def request_queue(self) -> 'Queue[Request]':
        return self._request_queue

    def run(self):
        self._logger.info('Communication running')

        if self._mqtt_connector:
            self._mqtt_connector.start()

        while 1:
            self._logger.info('Wait new request')
            request = self._request_queue.get()
            if request is not Request:
                logging.error('Not a request is stored in the queue')

            self._logger.info('New request receive from the queue. Start handle request')
            self.handle_request(request)

    def handle_request(self, request: Request):
        try:
            logging.info(f'Request {request.command_type}')
            if request.command_type == CommandType.SetPositions:
                self.handle_set_positions_request(request.payload)
                request.response_writer.write_response(Response(CommandType.Ok, None))

            if request.command_type == CommandType.SaveGesture:
                self.handle_save_gesture(request.payload)
                request.response_writer.write_response(Response(CommandType.Ok, None))

            if request.command_type == CommandType.DeleteGesture:
                self.handle_delete_gesture(request.payload)
                request.response_writer.write_response(Response(CommandType.Ok, None))

            if request.command_type == CommandType.PerformGestureId:
                self.handle_perform_gesture_by_id(request.payload)
                request.response_writer.write_response(Response(CommandType.Ok, None))

            if request.command_type == CommandType.PerformGestureRaw:
                self.handle_perform_gesture_raw(request.payload)
                request.response_writer.write_response(Response(CommandType.Ok, None))
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

    def handle_perform_gesture_raw(self, payload):
        logging.info(f'Start handling perform gesture raw')

        perform_gesture_raw_dto = PerformGestureRawDto()
        perform_gesture_raw_dto.deserialize(payload)

        self._hand_controller.perform_gesture(
            DtoToEntityConverter.convert_gesture_dto_to_gesture(perform_gesture_raw_dto.gesture_dto))
