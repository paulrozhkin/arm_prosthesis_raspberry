import logging
import time

from typing import Optional

import pickle

from rx import Observable
from rx.core import Observer

from arm_prosthesis.services.myoelectronics.preprocessing.feture_extactor import FeatureExtractor
from arm_prosthesis.utils.stoppable_thread import StoppableThread
from arm_prosthesis.services.myoelectronics.myoelectronics_sensor import MyoelectronicsSensor
from statistics import mean
from rx.subject import Subject


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

    _time: float = 0

    def _run(self):
        emg_value = self._sensor.get_value()

        pattern = self._emg_handler.handle(emg_value)

        if pattern is not None:
            self._pattern_subject.on_next(pattern)

        new_time = time.time()
        print(new_time - self._time)
        self._time = new_time


class EmgSignalHandler:
    _logger = logging.getLogger('Main')

    def __init__(self, knn_model):
        self._window = []
        self._signal = []
        self._is_signal = False
        self._limit = 400
        self._window_size = 3
        self._min_values_in_signal = 20

        self._knn_model = knn_model

    def handle(self, emg_value: int) -> Optional[int]:
        self._window.append(emg_value)

        if len(self._window) < self._window_size:
            return None

        self._window.pop(0)

        mean_in_window = mean(self._window)

        if self._is_signal:
            self._signal.append(emg_value)

            if mean_in_window <= self._limit:
                pattern = None
                signal_length = len(self._signal)
                if signal_length >= self._min_values_in_signal:
                    self._logger.info(f'New signal detected with length {signal_length}')
                    pattern = self._handle_signal(self._signal)
                else:
                    self._logger.info(f'Signal detected, but skip with length {signal_length}')

                self._signal.clear()
                self._window.clear()
                self._is_signal = False

                return pattern
        else:
            if mean_in_window >= self._limit:
                self._is_signal = True

        return None

    def _handle_signal(self, signal):
        mav_features = FeatureExtractor.extract_mav(signal)
        result = self._knn_model.predict([mav_features])

        return result


if __name__ == '__main__':
    reader = MyoelectronicsService()
    reader.start()
