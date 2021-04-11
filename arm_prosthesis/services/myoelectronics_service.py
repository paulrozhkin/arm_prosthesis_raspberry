import logging
import time
import Adafruit_ADS1x15

from arm_prosthesis.services.myoelectronics.myoelectronics_sensor import MyoelectronicsSensor


class MyoelectronicsService:
    _logger = logging.getLogger('Main')

    def __init__(self):
        self._sensor = MyoelectronicsSensor()

    def run(self):
        while True:
            start_time = time.time()
            values = self._sensor.get_value()
            print('| {0:>6} |'.format(values))
            # Pause for half a second.
            time.sleep(0.005)
            end_time = time.time()
            print(end_time - start_time)


if __name__ == '__main__':
    reader = MyoelectronicsService()
    reader.run()
