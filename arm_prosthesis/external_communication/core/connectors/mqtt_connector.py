import logging
import threading
import time
from queue import Queue

from bluedot.btcomm import BluetoothClient

from arm_prosthesis.config.configuration import Config
from arm_prosthesis.external_communication.models.request import Request


class MqttConnector(threading.Thread):
    _logger = logging.getLogger('Main')
    _mqtt_address: str
    _is_mqtt_connected: bool
    _bluetooth_client: BluetoothClient = None

    def __init__(self, config: Config, request_transmitter: 'Queue[Request]'):
        threading.Thread.__init__(self)
        self._config = config

        if not config.mqtt_enabled:
            self._logger.fatal('Mqtt is disabled but is trying to create')
            raise Exception('Mqtt is disabled but is trying to create')

        self._request_transmitter = request_transmitter
        self._mqtt_address = config.mqtt_address
        self._is_mqtt_connected = False

    def run(self):
        self._logger.info('Mqtt running start')
        self._bluetooth_client = BluetoothClient(server=self._mqtt_address, data_received_callback=self.data_received_handler,
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
        self._logger.debug(f'Receive {len(data)}: {data}')

    def send(self, payload: bytearray):
        if self._bluetooth_client is None:
            self._logger.critical('MQTT not running, but send invoke')
            raise ConnectionError('MQTT not running, but send invoke')

        self._bluetooth_client.send(payload)

