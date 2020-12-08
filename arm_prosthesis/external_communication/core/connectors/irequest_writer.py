from abc import ABCMeta, abstractmethod

from arm_prosthesis.external_communication.core.connectors.package_dto import PackageDto
from arm_prosthesis.external_communication.models.request import Request


class IPackageReceiver:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def receive_package(self, package: PackageDto): raise NotImplementedError
