# Press the green button in the gutter to run the script.
import sys
import threading
import time
import logging

from arm_prosthesis.external_communication.core.communication import Communication
from arm_prosthesis.hand_controller import HandController
from arm_prosthesis.config.configuration import load_config


class App:
    def __init__(self):
        self._config = load_config('./config/config.ini')
        self.init_logger()
        self._logger = logging.getLogger('Main')
        self._logger.info('Logger init. Start app.')
        self._logger.info(f'App settings:\n{self._config}')

        self._hand = HandController()
        self._communication = Communication(self._hand, self._config)

        self._communication_thread = threading.Thread(target=self._communication.run)
        self._hand_controller_thread = threading.Thread(target=self._hand.run)

    def run(self):
        self._logger.info('App start init workers.')

        self._communication_thread.start()
        self._hand_controller_thread.start()

        self._logger.info('App started.')
        self._hand_controller_thread.join()
        self._logger.info('App started.')

    def init_logger(self):
        session_name = time.strftime("%Y_%m_%d_%H_%M_%S")
        stdout_handler = logging.StreamHandler(sys.stdout)
        handlers = [stdout_handler]

        if self._config.log_to_file:
            log_file = self._config.path_to_log + '/' + session_name + '.log'
            print("Log file is: " + log_file)
            file_handler = logging.FileHandler(filename=log_file)
            handlers.append(file_handler)

        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)-8s [%(threadName)s] [%(filename)s:%(lineno)d] %(message)s',
            handlers=handlers
        )


if __name__ == '__main__':
    app = App()
    app.run()
