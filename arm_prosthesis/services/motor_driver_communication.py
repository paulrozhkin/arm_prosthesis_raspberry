import logging
import time
from queue import Queue
from typing import List

import crc8
import spidev

import enums_pb2 as enums
from arm_prosthesis.models.actuator_controller_queue import ActuatorControllerQueue, ActuatorControllerCommand
from arm_prosthesis.models.driver_telemetry import DriverTelemetry
from arm_prosthesis.models.motor_positions import MotorPositions
from arm_prosthesis.utils.stoppable_thread import StoppableThread


class ActuatorControllerService:
    _logger = logging.getLogger('Main')
    _default_interval = 0.5
    _telemetry_thread: StoppableThread = None

    def __init__(self):
        self._set_positions_queue: 'Queue[ActuatorControllerQueue]' = Queue()
        self._empty_payload = [0xFF] * 9
        self._telemetry_request = [0x00] * 9
        self._telemetry_request[8] = int.from_bytes(self._get_crc8_for_request(self._telemetry_request), "big")
        self._telemetry = DriverTelemetry(0, 0, 0, 0, 0, 0, 0)

    @property
    def telemetry(self) -> DriverTelemetry:
        return self._telemetry

    def enable_telemetry(self, interval_in_ms=None):
        if self._telemetry_thread is not None:
            raise Exception('Telemetry already started')

        if interval_in_ms is None:
            interval_seconds = self._default_interval
        else:
            interval_seconds = interval_in_ms / 1000

        if interval_seconds < 0:
            raise Exception('Incorrect interval')

        self._telemetry_thread = StoppableThread(self._telemetry_runner, interval_seconds)
        self._telemetry_thread.start()
        self._logger.info('Telemetry started')

    def disable_telemetry(self):
        if self._telemetry_thread is None:
            raise Exception('Telemetry not started')

        self._telemetry_thread.stop()
        self._telemetry_thread = None
        self._logger.info('Telemetry stopped')

    def _telemetry_runner(self):
        queue_command = ActuatorControllerQueue(ActuatorControllerCommand.TELEMETRY)
        self._set_positions_queue.put(queue_command)

    def run(self):
        spi = spidev.SpiDev()
        spi.open(0, 0)

        spi.bits_per_word = 8
        spi.max_speed_hz = 500000

        self._logger.info('Motor driver communication running')
        while 1:
            new_command: ActuatorControllerQueue
            new_command = self._set_positions_queue.get()

            requests: List[int]
            if new_command.command_type == ActuatorControllerCommand.SET_POSITIONS:
                self._logger.info('New positions receive from the queue. Send to driver')
                request = self._create_set_positions_request(new_command.motor_positions)
                logging.info(f"Send to driver: {request}")
            else:
                if new_command.command_type == ActuatorControllerCommand.TELEMETRY:
                    request = self._telemetry_request
                else:
                    raise Exception('Not supported')

            spi.xfer(request)
            time.sleep(0.02)

            # receive telemetry
            result = spi.xfer(self._empty_payload)

            self._set_telemetry(result)
            if new_command.command_type != ActuatorControllerCommand.TELEMETRY:
                logging.info(f"Receive from driver: {result}")

    def set_new_positions(self, positions: MotorPositions):
        queue_command = ActuatorControllerQueue(ActuatorControllerCommand.SET_POSITIONS, positions)
        self._set_positions_queue.put(queue_command)

    def _set_telemetry(self, response_driver: bytes):
        if response_driver[0] == 0:
            type_work = enums.DRIVER_STATUS_CONNECTION_ERROR

            crc_calculator = crc8.crc8()
            for i in range(0, len(response_driver)):
                crc_calculator.update(response_driver[i].to_bytes(1, 'little'))

            if response_driver[-1] == crc_calculator.digest():
                type_work = self._type_work_convert(response_driver[1])

            self._telemetry = DriverTelemetry(type_work, response_driver[2],
                                              response_driver[3], response_driver[4],
                                              response_driver[5], response_driver[6],
                                              response_driver[7])

    @staticmethod
    def _type_work_convert(state_code: int):
        if state_code == 0:
            return enums.DRIVER_STATUS_INITIALIZATION
        if state_code == 1:
            return enums.DRIVER_STATUS_ERROR
        if state_code == 2:
            return enums.DRIVER_STATUS_ERROR
        if state_code == 3:
            return enums.DRIVER_STATUS_SLEEP
        if state_code == 4:
            return enums.DRIVER_STATUS_SETTING_POSITION
        if state_code == 5:
            return enums.DRIVER_STATUS_ERROR

    @staticmethod
    def _get_crc8_for_request(request):
        crc_calculator = crc8.crc8()
        for i in range(0, len(request) - 1):
            crc_calculator.update(request[i].to_bytes(1, 'little'))

        return crc_calculator.digest()

    def _create_set_positions_request(self, positions: MotorPositions):
        protocol_driver_package = [0x00] * 9
        protocol_driver_package[0] = 1
        protocol_driver_package[1] = 0
        protocol_driver_package[2] = positions.little_finger_angle_position
        protocol_driver_package[3] = positions.ring_finger_angle_position
        protocol_driver_package[4] = positions.middle_finger_angle_position
        protocol_driver_package[5] = positions.index_finger_angle_position
        protocol_driver_package[6] = positions.thumb_finger_angle_position
        protocol_driver_package[7] = positions.thumb_ejector_angle_position
        protocol_driver_package[8] = int.from_bytes(self._get_crc8_for_request(protocol_driver_package),
                                                    byteorder="big")
        return protocol_driver_package
