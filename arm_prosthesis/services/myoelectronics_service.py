import logging
import time

from arm_prosthesis.utils.stoppable_thread import StoppableThread
from arm_prosthesis.services.myoelectronics.myoelectronics_sensor import MyoelectronicsSensor


class MyoelectronicsService:
    _logger = logging.getLogger('Main')

    _executor: StoppableThread = None

    def __init__(self):
        self._sensor = MyoelectronicsSensor()

    def start(self):
        if self._executor is not None:
            raise Exception("Service already started.")

        self._executor = StoppableThread(self._run)
        self._executor.run()
        self._logger.info('[MyoelectronicsService] started')

    def stop(self):
        if self._executor is None:
            raise Exception("Service not started.")

        self._executor.stop()
        self._executor = None
        self._logger.info('[MyoelectronicsService] stopped')

    _time: float = 0

    def _run(self):
        # start_time = time.time()
        values = self._sensor.get_value()
        print('| {0:>6} |'.format(values))
        # Pause for half a second.
        # end_time = time.time()
        new_time = time.time()
        print(new_time - self._time)
        self._time = new_time


if __name__ == '__main__':
    reader = MyoelectronicsService()
    reader.start()
