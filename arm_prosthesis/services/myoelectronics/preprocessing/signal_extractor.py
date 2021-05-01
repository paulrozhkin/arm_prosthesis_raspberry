import os
from scipy.stats.mstats import gmean
import csv


class SignalExtractor:

    @staticmethod
    def extract_from_directory(directory_source, directory_dist):
        for file_name in os.listdir(directory_source):
            full_file_path = directory_source + file_name
            dist_full_file_path = directory_dist + file_name
            SignalExtractor.extract_from_file(full_file_path, dist_full_file_path)

    @staticmethod
    def extract_from_file(full_file_path, dist_full_file_path):
        window = []
        signal = []
        is_signal = False
        limit = 400
        window_size = 5

        with open(full_file_path, newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            next(reader, None)  # skip the headers

            for row in reader:
                adc_value = int(row[1])
                window.append(adc_value)

                if len(window) < window_size:
                    continue

                window.pop(0)
                geometric_mean_in_window = gmean(window)

                if is_signal:
                    signal.append(row)

                    if geometric_mean_in_window <= limit:
                        is_signal = False
                        break
                else:
                    if geometric_mean_in_window >= limit:
                        is_signal = True

        with open(dist_full_file_path, 'w', newline='') as csv_file:
            fieldnames = ['tick', 'adc']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')

            writer.writeheader()

            for row in signal:
                writer.writerow({'tick': row[0], 'adc': row[1]})


if __name__ == '__main__':
    project_directory = 'C:/DATA/MyProject/BigProjects/ProjectHand/hand/arm_prosthesis_raspberry/data/gestures/'

    gestures_directory_name = 'clenching'
    gestures_directory_source = project_directory + gestures_directory_name + '/'
    gestures_directory_dist = project_directory + gestures_directory_name + '_extracted/'

    # SignalExtractor.extract_from_file(gestures_directory_source + '2021_04_04_17_44_00.csv',
    #                                   gestures_directory_dist + '2021_04_04_17_44_00.csv')

    SignalExtractor.extract_from_directory(gestures_directory_source, gestures_directory_dist)
