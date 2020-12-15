import logging
import time
from queue import Queue

import spidev

from arm_prosthesis.models.motor_positions import MotorPositions


class MotorDriverCommunication:
    _logger = logging.getLogger('Main')

    def __init__(self):
        self._set_positions_queue: 'Queue[MotorPositions]' = Queue()

    def run(self):
        spi = spidev.SpiDev()
        spi.open(0, 0)

        spi.bits_per_word = 8
        spi.max_speed_hz = 500000

        self._logger.info('Motor driver communication running')
        while 1:
            self._logger.info('Wait new command')
            positions: MotorPositions = self._set_positions_queue.get()
            self._logger.info('New positions receive from the queue. Send to driver')

            protocol_driver_package = [0x00] * 27
            protocol_driver_package[0] = 1
            protocol_driver_package[1] = 0
            protocol_driver_package[2] = positions.little_finger_angle_position
            protocol_driver_package[3] = positions.ring_finger_angle_position
            protocol_driver_package[4] = positions.middle_finger_angle_position
            protocol_driver_package[5] = positions.index_finger_angle_position
            protocol_driver_package[6] = positions.thumb_finger_angle_position
            protocol_driver_package[7] = positions.thumb_ejector_angle_position
            logging.info(f"Send to driver: {protocol_driver_package}")
            spi.xfer(protocol_driver_package)

            time.sleep(0.01)

            # receive telemetry
            empty = [0xFF] * 27
            result = spi.xfer(empty)
            logging.info(f"Receive from driver: {result}")

    def set_new_positions(self, positions: MotorPositions):
        self._set_positions_queue.put(positions)
