import unittest

from arm_prosthesis.services.myoelectronics.preprocessing.feture_extactor import FeatureExtractor


class TestFeatureExtractor(unittest.TestCase):
    def test_mav_extract(self):
        # Given
        signal = list(range(100))

        # When
        result = FeatureExtractor.extract_mav(signal)

        # Then
        assert result[0] == 4.5
        assert result[9] == 94.5


if __name__ == '__main__':
    unittest.main()
