class SignalSampler:

    @staticmethod
    def sampling(signal: [int], count_of_samples: int = 10) -> [[int]]:
        # signal_length = len(signal)
        # value_in_samples = int(signal_length / count_of_samples)
        return SignalSampler._split_list(signal, count_of_samples)

    @staticmethod
    def _split_list(inner_list, wanted_parts=1):
        length = len(inner_list)
        return [inner_list[i * length // wanted_parts: (i + 1) * length // wanted_parts]
                for i in range(wanted_parts)]
