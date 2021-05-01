import unittest
from arm_prosthesis.services.myoelectronics.preprocessing.signal_sampler import SignalSampler


class TestSignalSampler(unittest.TestCase):
    def test_sampling(self):
        # Given
        signal = list(range(117))

        # When
        result = SignalSampler.sampling(signal)

        # Then
        assert len(result) == 10
        assert len(result[0]) == 11


if __name__ == '__main__':
    unittest.main()
