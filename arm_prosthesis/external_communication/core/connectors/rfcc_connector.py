import logging
import threading
import time
from queue import Queue

from bluedot.btcomm import BluetoothServer

from arm_prosthesis.config.configuration import Config
from arm_prosthesis.external_communication.core.connectors.irequest_writer import IPackageReceiver
from arm_prosthesis.external_communication.core.connectors.iresponse_writer import IResponseWriter
from arm_prosthesis.external_communication.core.connectors.package_dto import PackageDto
from arm_prosthesis.external_communication.core.protocol_parser import ProtocolParser
from arm_prosthesis.external_communication.models.command_type import CommandType
from arm_prosthesis.external_communication.models.request import Request
from arm_prosthesis.external_communication.models.response import Response


class RFCCConnector(threading.Thread, IResponseWriter, IPackageReceiver):
    _logger = logging.getLogger('Main')
    _bluetooth_server: BluetoothServer = None
    _response_mutex = threading.Lock()
    _count_connected: int

    def __init__(self, config: Config, request_transmitter: 'Queue[Request]'):
        threading.Thread.__init__(self)
        self._config = config

        if not config.rfcomm_enabled:
            self._logger.fatal('RFCC is disabled but is trying to create')
            raise Exception('RFCC is disabled but is trying to create')

        self._count_connected = 0
        self._request_transmitter = request_transmitter
        self._protocol_parser = ProtocolParser(self)

    @property
    def connected(self) -> bool:
        if self._bluetooth_server is not None:
            return self._count_connected > 0
        else:
            return False

    def run(self):
        self._logger.info('RFCC running start')
        self._bluetooth_server = BluetoothServer(data_received_callback=self._data_received_handler,
                                                 auto_start=False, power_up_device=True, encoding=None,
                                                 when_client_connects=self._client_connect_handler,
                                                 when_client_disconnects=self._client_disconnect_handler)
        self._logger.info('RFCC server created')

        while True:
            self._logger.info('RFCC server try to start')
            try:
                self._bluetooth_server.start()
            except OSError as e:
                self._logger.info(f'RFCC server start error: {e}')
                time.sleep(30)
                continue
            except Exception as e:
                self._logger.exception(e)
                raise e

            self._logger.info('RFCC started')
            break

    def _client_connect_handler(self):
        self._logger.info('New device connected')
        self._count_connected = self._count_connected + 1

    def _client_disconnect_handler(self):
        self._logger.info('Device disconnected')
        self._count_connected = self._count_connected - 1

        if self._count_connected < 0:
            self._count_connected = 0

    def _data_received_handler(self, data):
        self._logger.debug(f'RFCC receive {len(data)} bytes')
        self._protocol_parser.update(data)

    def write_response(self, response: Response):
        self._response_mutex.acquire()

        payload_length = 0
        if response.payload is not None:
            payload_length = {len(response.payload)}

        if response.command_type is not CommandType.Telemetry:
            self._logger.info(
                f'RFCC try to send response with type {response.command_type} and payload length {payload_length}')
        package = self._protocol_parser.create_package(response.command_type, response.payload)
        self.send(self._protocol_parser.serialize_package(package))

        self._response_mutex.release()

    def receive_package(self, package: PackageDto):
        self._logger.info(f'RFCC receive new package {package.command_type} with size {package.payload_size} bytes')
        new_request = Request(package.command_type, package.payload, self)
        self._request_transmitter.put(new_request)

    def send(self, payload: bytes):
        if self._bluetooth_server is None:
            self._logger.critical('RFCC not running, but send invoke')
            raise ConnectionError('RFCC not running, but send invoke')

        self._bluetooth_server.send(payload)
