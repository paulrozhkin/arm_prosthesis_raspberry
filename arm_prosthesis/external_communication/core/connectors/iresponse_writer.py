from abc import ABCMeta, abstractmethod
from arm_prosthesis.external_communication.models.response import Response


class IResponseWriter:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def write_response(self, response: Response): raise NotImplementedError
