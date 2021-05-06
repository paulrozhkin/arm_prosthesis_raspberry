import threading


class StoppableThread(threading.Thread):

    def __init__(self, target, timeout = None):
        super(StoppableThread, self).__init__()
        self._target = target
        self._timeout = timeout
        self._stop = threading.Event()

    def run(self):
        while not self.stopped():
            if self._timeout is not None:
                self._stop.wait(self._timeout)  # instead of sleeping

            if self.stopped():
                continue
            self._target()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
