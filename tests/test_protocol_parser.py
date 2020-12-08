import time
import unittest
from unittest.mock import MagicMock

from arm_prosthesis.external_communication.core.protocol_parser import ProtocolParser, ProtocolState
from arm_prosthesis.external_communication.models.command_type import CommandType


class TestProtocolParser(unittest.TestCase):

    def test_sfd_receive_correct(self):
        # Given
        self._package_receiver_mock = MagicMock()
        parser = ProtocolParser(self._package_receiver_mock)
        incorrect_received = bytes(b'\x03\x5B\xD5\xD4')
        sfd_part1_received = bytes(b'\xfd\xba\xdc')
        sfd_part2_received = bytes(b'\x01\x50\xb4\x11\xff')

        # When
        parser.update(incorrect_received)
        parser.update(sfd_part1_received)
        parser.update(sfd_part2_received)

        # Then
        assert parser.state == ProtocolState.TYPE

    def test_receive_incorrect_sfd(self):
        # Given
        parser = ProtocolParser(MagicMock())
        first_received = bytes(b'\x03\x5B\xD5\xD4')
        second_received = bytes(b'\xff\xfa\xb4')
        third_received = bytes(b'\x01\x50\xb4\x11\xff')

        # When
        parser.update(first_received)
        parser.update(second_received)
        parser.update(third_received)

        # Then
        assert parser.state == ProtocolState.SFD

    def test_receive_type(self):
        # Given
        parser = ProtocolParser(MagicMock())
        sfd_received = bytes(b'\xfd\xba\xdc\x01\x50\xb4\x11\xff')
        type_received = bytes(b'\x09')

        # When
        parser.update(sfd_received)
        parser.update(type_received)

        # Then
        assert parser.state == ProtocolState.SIZE
        assert parser.current_request.command_type == CommandType.PerformGestureId

    def test_receive_size(self):
        # Given
        parser = ProtocolParser(MagicMock())
        sfd_received = bytes(b'\xfd\xba\xdc\x01\x50\xb4\x11\xff')
        type_received = bytes(b'\x09')
        size_received = bytes(b'\x3b\x01')

        # When
        parser.update(sfd_received)
        parser.update(type_received)
        parser.update(size_received)

        # Then
        assert parser.state == ProtocolState.PAYLOAD
        assert parser.current_request.payload_size == 315

    def test_receive_package(self):
        # Given
        receiver_mock = MagicMock()
        parser = ProtocolParser(receiver_mock)
        sfd_part1_received = bytes(b'\xfd\xba\xdc')
        sfd_part2_third_received = bytes(b'\x01\x50\xb4\x11\xff')
        type_info_payload_crc8_received = bytes(b'\x09\x05\x00\xff\xff\xff\xff\xff\xb6')

        # When
        parser.update(sfd_part1_received)
        parser.update(sfd_part2_third_received)
        parser.update(type_info_payload_crc8_received)

        # Then
        assert parser.state == ProtocolState.SFD
        assert parser.current_request.payload_size == 5
        assert parser.current_request.payload == bytes(b'\xff\xff\xff\xff\xff')
        assert parser.current_request.command_type == CommandType.PerformGestureId
        assert parser.current_request.received_crc8 == b'\xb6'
        assert parser.current_request.real_crc8 == b'\xc6'
        assert receiver_mock.receive_package.call_count == 1

    def test_receive_sequence_package(self):
        # Given

        parser = ProtocolParser(MagicMock())
        package1_received = bytes(b'\xfd\xba\xdc\x01\x50\xb4\x11\xff\x09\x05\x00\xff\xff\xff\xff\xff\xb6')
        package2_received = bytes(b'\xfd\xba\xdc\x01\x50\xb4\x11\xff\x05\x02\x00\xab\xcd\x8a')

        # When & Then
        parser.update(package1_received)

        assert parser.state == ProtocolState.SFD
        assert parser.current_request.payload_size == 5
        assert parser.current_request.payload == bytes(b'\xff\xff\xff\xff\xff')
        assert parser.current_request.command_type == CommandType.PerformGestureId
        assert parser.current_request.received_crc8 == b'\xb6'
        assert parser.current_request.real_crc8 == b'\xc6'

        parser.update(package2_received)

        assert parser.state == ProtocolState.SFD
        assert parser.current_request.payload_size == 2
        assert parser.current_request.payload == bytes(b'\xab\xcd')
        assert parser.current_request.command_type == CommandType.SetSettings
        assert parser.current_request.received_crc8 == b'\x8a'
        assert parser.current_request.real_crc8 == b'\x23'

    def test_create_package(self):
        # Given
        command = CommandType.GetGestures
        payload = bytes(b'\xba\x05')

        # When
        package = ProtocolParser.create_package(command, payload)

        # Then
        assert command == package.command_type
        assert payload == package.payload
        assert len(payload) == package.payload_size

    def test_create_package_with_empty_payload(self):
        # Given
        command = CommandType.GetGestures

        # When
        package = ProtocolParser.create_package(command, None)

        # Then
        assert command == package.command_type
        assert package.payload is None
        assert 0 == package.payload_size

    def test_serialize(self):
        # Given
        command = CommandType.GetGestures
        payload = bytes(b'\xba\x05')

        expected_bytes = bytes(b'\xfd\xba\xdc\x01\x50\xb4\x11\xff\x06\x02\x00\xba\x05\xb1')

        parser = ProtocolParser(MagicMock())

        # When
        package = ProtocolParser.create_package(command, payload)
        ser_package = parser.serialize_package(package)

        # Then
        assert expected_bytes == ser_package

    def test_serialize_with_empty_payload(self):
        # Given
        command = CommandType.GetSettings
        payload = None

        expected_bytes = bytes(b'\xfd\xba\xdc\x01\x50\xb4\x11\xff\x04\x00\x00\xab')

        parser = ProtocolParser(MagicMock())

        # When
        package = ProtocolParser.create_package(command, payload)
        ser_package = parser.serialize_package(package)

        # Then
        assert expected_bytes == ser_package

    def test_timeout(self):
        # Given
        receiver_mock = MagicMock()
        parser = ProtocolParser(receiver_mock)
        sfd_received = bytes(b'\xfd\xba\xdc\x01\x50\xb4\x11\xff')
        before_timeout_received = bytes(b'\x09\x05\x00\xff')

        package_after_timeout_received = bytes(b'\xfd\xba\xdc\x01\x50\xb4\x11\xff\x09\x05\x00\xff\xff\xff\xff\xff\xb6')

        # When & Then
        parser.update(sfd_received)
        parser.update(before_timeout_received)

        assert parser.state == ProtocolState.PAYLOAD
        time.sleep(6)

        parser.update(package_after_timeout_received)

        assert parser.state == ProtocolState.SFD
        assert parser.current_request.payload_size == 5
        assert parser.current_request.payload == bytes(b'\xff\xff\xff\xff\xff')
        assert parser.current_request.command_type == CommandType.PerformGestureId
        assert parser.current_request.received_crc8 == b'\xb6'
        assert parser.current_request.real_crc8 == b'\xc6'


if __name__ == '__main__':
    unittest.main()
