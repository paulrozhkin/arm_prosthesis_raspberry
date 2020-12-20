import unittest
import crc8


class TestCrc8(unittest.TestCase):
    def test_crc8_calculate(self):
        # Given
        data = [b'\x04', b'\x03', b'\xFB', b'\xAD', b'\xFF', b'\xBD']
        expected_crc8 = b'\xBF'

        # When
        hash = crc8.crc8()
        for byte in data:
            hash.update(byte)

        # Then
        assert hash.digest() == expected_crc8


if __name__ == '__main__':
    unittest.main()
