from statistics import mean

from typing import Optional

import logging

from arm_prosthesis.services.myoelectronics.preprocessing.feture_extactor import FeatureExtractor


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
