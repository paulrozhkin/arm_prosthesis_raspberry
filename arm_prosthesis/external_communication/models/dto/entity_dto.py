from abc import ABC, abstractmethod


class EntityDto(ABC):

    @abstractmethod
    def serialize(self) -> bytes: raise NotImplementedError

    @abstractmethod
    def deserialize(self, byte_array: bytes): raise NotImplementedError
