import csv
import time
from os import path

from arm_prosthesis.services.myoelectronics.myoelectronics_sensor import MyoelectronicsSensor


class MyoelectronicsRecorder:
    def __init__(self, path_to_records: str):
        if not path.exists(path_to_records):
            raise Exception("Path to records not exist")

        if not path.isdir(path_to_records):
            raise Exception("Path to records is not directory")

        session_name = time.strftime("%Y_%m_%d_%H_%M_%S")
        self._path_to_record_file_csv = path.join(path_to_records, session_name + '.csv')
        print('Path to records: ' + self._path_to_record_file_csv)

        self._sensor = MyoelectronicsSensor()

    def record(self):
        self._sensor.start_sensor()

        print("Session started. For interrupt press `CTRL+C`.")
        records = []
        tick = 0
        while True:
            try:
                # start_time = time.time()
                value = self._sensor.get_value()
                print(value)
                records.append({'tick': tick, 'adc': value})
                tick += 1
                # print('| {0:>6} |'.format(values))
                # Pause for half a second.
                # end_time = time.time()
                # print(end_time - start_time)
            except KeyboardInterrupt:
                print("\nSession aborted")
                break

        self._sensor.stop_sensor()

        print("Session start writing")
        with open(self._path_to_record_file_csv, 'w', newline='') as csv_file:
            fieldnames = ['tick', 'adc']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')

            writer.writeheader()

            for row in records:
                writer.writerow(row)
        print("Writing end")


if __name__ == '__main__':
    reader = MyoelectronicsRecorder('/home/pi/arm-prosthesis-bin/records')
    reader.record()
