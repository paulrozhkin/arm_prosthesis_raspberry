from arm_prosthesis.external_communication.models.dto.entity_dto import EntityDto


class SetSettingsDto(EntityDto):
    def serialize(self) -> bytearray:
        pass

    def deserialize(self, byte_array: bytearray):
        pass
