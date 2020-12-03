from abc import ABC, abstractmethod


class EntityDto(ABC):

    @abstractmethod
    def serialize(self) -> bytearray: raise NotImplementedError

    @abstractmethod
    def deserialize(self, byte_array: bytearray): raise NotImplementedError
