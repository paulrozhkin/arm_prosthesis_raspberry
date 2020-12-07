import logging
import sys
from queue import Queue

from arm_prosthesis.config.configuration import Config
from arm_prosthesis.external_communication.core.connectors.mqtt_connector import MqttConnector
from arm_prosthesis.external_communication.models.command_type import CommandType
from arm_prosthesis.external_communication.models.dto.set_positions_dto import SetPositionsDto
from arm_prosthesis.external_communication.models.request import Request
from arm_prosthesis.external_communication.models.response import Response
from arm_prosthesis.hand_controller import HandController
from arm_prosthesis.models.positions import Positions


class Communication:
    _logger = logging.getLogger('Main')

    def __init__(self, hand_controller: HandController, config: Config):
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
            self._mqtt_connector.run()

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
        except:
            e = sys.exc_info()[0]
            logging.error(f'Error request handling: {e}')
            error_response = Response(CommandType.Error)
            request.response_writer.write_response(error_response)

    def handle_set_positions_request(self, payload: bytearray):
        logging.info(f'Start handling set positions')
        set_position = SetPositionsDto()
        set_position.deserialize(payload)
        positions = Positions(set_position.little_finger_position, set_position.ring_finger_position,
                              set_position.middle_finger_position, set_position.index_finger_position,
                              set_position.thumb_finger_position)
        self._hand_controller.set_positions(positions)
