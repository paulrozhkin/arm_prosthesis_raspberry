from typing import List

from arm_prosthesis.services.myoelectronics.preprocessing.signal_sampler import SignalSampler


class FeatureExtractor:

    # Extract Mean absolute value (MAV)
    @staticmethod
    def extract_mav(signal: List[int]) -> List[float]:
        mav_result = []

        samples = SignalSampler.sampling(signal)
        for sample in samples:
            mav_result.append(FeatureExtractor._calculate_mav(sample))

        return mav_result

    @staticmethod
    def _calculate_mav(sample: List[int]) -> float:
        sum_abs_numbers = 0
        for t in sample:
            sum_abs_numbers = sum_abs_numbers + abs(t)

        mav = sum_abs_numbers / len(sample)
        return mav
