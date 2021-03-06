import logging
import threading
import time
from queue import Queue

from bluedot.btcomm import BluetoothClient

from arm_prosthesis.config.configuration import Config
from arm_prosthesis.external_communication.core.connectors.irequest_writer import IPackageReceiver
from arm_prosthesis.external_communication.core.connectors.iresponse_writer import IResponseWriter
from arm_prosthesis.external_communication.core.connectors.package_dto import PackageDto
from arm_prosthesis.external_communication.core.protocol_parser import ProtocolParser
from arm_prosthesis.external_communication.models.command_type import CommandType
from arm_prosthesis.external_communication.models.request import Request
from arm_prosthesis.external_communication.models.response import Response


class MqttConnector(threading.Thread, IResponseWriter, IPackageReceiver):
    _logger = logging.getLogger('Main')
    _mqtt_address: str
    _is_mqtt_connected: bool
    _bluetooth_client: BluetoothClient = None
    _response_mutex = threading.Lock()

    def __init__(self, config: Config, request_transmitter: 'Queue[Request]'):
        threading.Thread.__init__(self)
        self._config = config

        if not config.mqtt_enabled:
            self._logger.fatal('Mqtt is disabled but is trying to create')
            raise Exception('Mqtt is disabled but is trying to create')

        self._request_transmitter = request_transmitter
        self._mqtt_address = config.mqtt_address
        self._is_mqtt_connected = False
        self._protocol_parser = ProtocolParser(self)

    @property
    def connected(self) -> bool:
        if self._bluetooth_client is not None:
            return self._bluetooth_client.connected
        else:
            return False

    def run(self):
        self._logger.info('Mqtt running start')
        self._bluetooth_client = BluetoothClient(server=self._mqtt_address,
                                                 data_received_callback=self.data_received_handler,
                                                 auto_connect=False, power_up_device=True, encoding=None)
        self._logger.info('Mqtt client created')

        while True:
            self._logger.info('Mqtt client try to connect')
            try:
                self._bluetooth_client.connect()
            except OSError as e:
                self._logger.info(f'Mqtt client connection error: {e}')
                time.sleep(30)
                continue
            except Exception as e:
                self._logger.exception(e)
                raise e

            self._is_mqtt_connected = True
            self._logger.info('Mqtt client connected')

            while True:
                if not self._bluetooth_client.connected:
                    self._logger.info('Mqtt client disconnected')
                    self._is_mqtt_connected = False
                    break

                self._is_mqtt_connected = False

            time.sleep(10)

    def data_received_handler(self, data):
        self._logger.debug(f'MQTT receive {len(data)} bytes')
        self._protocol_parser.update(data)

    def write_response(self, response: Response):
        self._response_mutex.acquire()

        payload_length = 0
        if response.payload is not None:
            payload_length = {len(response.payload)}

        if response.command_type is not CommandType.Telemetry:
            self._logger.info(
                f'MQTT try to send response with type {response.command_type} and payload length {payload_length}')
        package = self._protocol_parser.create_package(response.command_type, response.payload)
        self.send(self._protocol_parser.serialize_package(package))

        self._response_mutex.release()

    def receive_package(self, package: PackageDto):
        self._logger.info(f'MQTT receive new package {package.command_type} with size {package.payload_size} bytes')
        new_request = Request(package.command_type, package.payload, self)
        self._request_transmitter.put(new_request)

    def send(self, payload: bytes):
        if self._bluetooth_client is None:
            self._logger.critical('MQTT not running, but send invoke')
            raise ConnectionError('MQTT not running, but send invoke')

        self._bluetooth_client.send(payload)
