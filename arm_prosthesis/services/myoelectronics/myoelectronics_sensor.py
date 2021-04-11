import logging
import Adafruit_ADS1x15


class MyoelectronicsSensor:
    _logger = logging.getLogger('Main')

    _ADS1x15_CONFIG_GAIN = [
        2 / 3,  # ±6.144 V, 187.5 μV
        1,  # ±4.096 V, 125 μV
        2,  # ±2.048 V, 62.5 μV
        4,  # ±1.024 V, 31.25 μV
        8,  # ±0.512 V, 15.625 μV
        16  # ±0.256 V, 7.8125 μV
    ]

    _MAXIMUM_VALUE_FOR_12BIT = 4095

    def __init__(self):
        # Create an ADS1115 ADC (16-bit) instance.
        self._adc = Adafruit_ADS1x15.ADS1115()
        self._adc.stop_adc()

        self._CHANNEL = 0
        self._GAIN = self._ADS1x15_CONFIG_GAIN[0]
        self._RATE = 475

        # For 5 volts - maximum value is:
        if self._ADS1x15_CONFIG_GAIN[0] == self._GAIN:
            self._maximum_value_for_16_bit_and_5v = int(5000000 / 187.5)
        else:
            self._logger.info("Conversation for sensor not supported.")
            raise Exception('Conversation not supported')

        self._coefficient_conversation = self._MAXIMUM_VALUE_FOR_12BIT / self._maximum_value_for_16_bit_and_5v

    def start_sensor(self):
        self._logger.info("Sensor try to start.")
        self._adc.start_adc(self._CHANNEL, self._GAIN, self._RATE)
        self._logger.info("Sensor running.")

    def stop_sensor(self):
        self._adc.stop_adc()

    def get_value(self) -> int:
        value_from_sensor = self._adc.get_last_result()
        result = self._conversation_to_12bit(value_from_sensor)
        return result

    def _conversation_to_12bit(self, value_from_16_bit_sensor: int) -> int:
        if value_from_16_bit_sensor > self._maximum_value_for_16_bit_and_5v:
            value_from_16_bit_sensor = self._maximum_value_for_16_bit_and_5v

        if value_from_16_bit_sensor < 0:
            value_from_16_bit_sensor = 0

        return int(value_from_16_bit_sensor * self._coefficient_conversation)

