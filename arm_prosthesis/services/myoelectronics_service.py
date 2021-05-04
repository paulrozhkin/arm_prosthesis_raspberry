import logging
import pickle
import time

from rx import Observable
from rx.subject import Subject

from arm_prosthesis.services.myoelectronics.emg_signal_handler import EmgSignalHandler
from arm_prosthesis.services.myoelectronics.myoelectronics_sensor import MyoelectronicsSensor
from arm_prosthesis.utils.stoppable_thread import StoppableThread


class MyoelectronicsService:
    _logger = logging.getLogger('Main')

    _executor: StoppableThread = None

    def __init__(self, path_to_model):
        self._sensor = MyoelectronicsSensor()
        self._pattern_subject = Subject()

        self._logger.info('Start loading pattern model')
        self._loaded_model = pickle.load(open(path_to_model, 'rb'))
        self._emg_handler = EmgSignalHandler(self._loaded_model)
        self._logger.info('Patterns model loading')

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

    @property
    def pattern_observable(self) -> 'Observable':
        return self._pattern_subject

    def _run(self):
        emg_value = self._sensor.get_value()

        pattern = self._emg_handler.handle(emg_value)

        if pattern is not None:
            self._pattern_subject.on_next(pattern)


if __name__ == '__main__':
    path_to_model = ''
    reader = MyoelectronicsService(path_to_model)
    reader.start()
