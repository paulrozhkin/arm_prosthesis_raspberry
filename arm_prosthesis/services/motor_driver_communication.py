import logging
import time
from queue import Queue, Empty

import crc8
import spidev

from arm_prosthesis.models.driver_telemetry import DriverTelemetry
from arm_prosthesis.models.motor_positions import MotorPositions
import enums_pb2 as enums


class MotorDriverCommunication:
    _logger = logging.getLogger('Main')

    def __init__(self):
        self._set_positions_queue: 'Queue[MotorPositions]' = Queue()
        self._empty_payload = [0xFF] * 9
        self._telemetry_request = [0x00] * 9
        self._telemetry_request[8] = int.from_bytes(self._get_crc8_for_request(self._telemetry_request), "big")
        self._telemetry = DriverTelemetry(0, 0, 0, 0, 0, 0, 0)

    @property
    def telemetry(self) -> DriverTelemetry:
        return self._telemetry

    def run(self):
        spi = spidev.SpiDev()
        spi.open(0, 0)

        spi.bits_per_word = 8
        spi.max_speed_hz = 500000

        self._logger.info('Motor driver communication running')
        while 1:
            try:
                positions: MotorPositions = self._set_positions_queue.get(timeout=0.5)
                self._logger.info('New positions receive from the queue. Send to driver')

                protocol_driver_package = [0x00] * 9
                protocol_driver_package[0] = 1
                protocol_driver_package[1] = 0
                protocol_driver_package[2] = positions.little_finger_angle_position
                protocol_driver_package[3] = positions.ring_finger_angle_position
                protocol_driver_package[4] = positions.middle_finger_angle_position
                protocol_driver_package[5] = positions.index_finger_angle_position
                protocol_driver_package[6] = positions.thumb_finger_angle_position
                protocol_driver_package[7] = positions.thumb_ejector_angle_position
                protocol_driver_package[8] = self._get_crc8_for_request(protocol_driver_package)
                logging.info(f"Send to driver: {protocol_driver_package}")
                spi.xfer(protocol_driver_package)

                time.sleep(0.02)

                # receive telemetry
                result = spi.xfer(self._empty_payload)
                logging.info(f"Receive from driver: {result}")
                self._set_telemetry(result)
            except Empty as error:
                # receive telemetry
                spi.xfer(self._telemetry_request)
                time.sleep(0.02)
                result = spi.xfer(self._empty_payload)
                self._set_telemetry(result)

    def set_new_positions(self, positions: MotorPositions):
        self._set_positions_queue.put(positions)

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
