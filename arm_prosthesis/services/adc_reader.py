import logging
import time
import Adafruit_ADS1x15


class AdcReader:
    _logger = logging.getLogger('Main')

    def __init__(self):
        # Create an ADS1115 ADC (16-bit) instance.
        self._adc = Adafruit_ADS1x15.ADS1115()
        self._adc.stop_adc()
        self._GAIN = 2/3

    def run(self):
        self._logger.info("Adc reader try to start.")
        self._adc.start_adc(0, 2/3, 475)
        self._logger.info("Adc reader running.")
        # Print nice chanel column headers.
        # Main loop.
        while True:
            start_time = time.time()
            values = self._adc.get_last_result()
            # print('| {0:>6} |'.format(values))
            # Pause for half a second.
            time.sleep(0.005)
            end_time = time.time()
            #print(end_time - start_time)


if __name__ == '__main__':
    reader = AdcReader()
    reader.run()
