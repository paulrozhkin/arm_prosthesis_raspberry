import csv
import os
import pickle
from math import sqrt
from typing import Dict

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor

from arm_prosthesis.services.myoelectronics.preprocessing.feture_extactor import FeatureExtractor

gestures_signals_names = {
    0: 'clenching',
    1: 'sharp_flexion'
}


class ClassificationTraining:
    def __init__(self):
        pass

    def train(self, tagged_signals: Dict[int, str], output_model_path: str):
        features_inputs = []
        output = []

        for signal_tag in tagged_signals:
            signal_dir_path = tagged_signals[signal_tag]
            for file_name in os.listdir(signal_dir_path):
                # get the original signal
                signal_data = self.extract_signal_from_csv(signal_dir_path + file_name)

                # get mav feature from signal
                mav_features = FeatureExtractor.extract_mav(signal_data)
                features_inputs.append(mav_features)
                output.append(signal_tag)

        # split the sample into test and training
        features_train, features_test, output_train, output_test = train_test_split(
            features_inputs, output, test_size=0.2, random_state=12345
        )

        # create and train model
        knn_model = KNeighborsRegressor(n_neighbors=2)
        knn_model.fit(features_train, output_train)

        # test model

        # Get of Root Mean Square Error (RMSE)
        print("Train RMSE:" + str(ClassificationTraining.calculate_rmse(knn_model, features_train, output_train)))
        print("Test RMSE:" + str(ClassificationTraining.calculate_rmse(knn_model, features_test, output_test)))

        # Save model
        with open(output_model_path, 'wb') as knn_file:
            pickle.dump(knn_model, knn_file)

    @staticmethod
    def calculate_rmse(knn_model, input_model, output_model):
        train_predicts = knn_model.predict(input_model)
        mse = mean_squared_error(output_model, train_predicts)
        rmse = sqrt(mse)
        return rmse

    @staticmethod
    def extract_signal_from_csv(file_signal_path: str):
        signal = []
        with open(file_signal_path, newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            next(reader, None)  # skip the headers

            for row in reader:
                signal.append(int(row[1]))

        return signal


if __name__ == '__main__':
    path_to_gestures = '//home/pi/arm-prosthesis/data/gestures/training/'
    model_path = '//home/pi/arm-prosthesis-bin/knn_model'

    tagged_gestures = {}
    for gesture_id in gestures_signals_names:
        gesture_name = gestures_signals_names[gesture_id]
        gesture_path = path_to_gestures + gesture_name + '/'
        tagged_gestures[gesture_id] = gesture_path

    classification_trainer = ClassificationTraining()
    classification_trainer.train(tagged_gestures, model_path)
