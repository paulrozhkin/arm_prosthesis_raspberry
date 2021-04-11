import pickle
import logging

from arm_prosthesis.services.myoelectronics.classification.classification_training import ClassificationTraining
from arm_prosthesis.services.myoelectronics.preprocessing.feture_extactor import FeatureExtractor


class ClassificationPredictor:
    _logger = logging.getLogger('Main')

    def __init__(self, path_to_model):
        # load the model from disk
        self._loaded_model = pickle.load(open(path_to_model, 'rb'))

    def predict(self, signal_data):
        mav_features = FeatureExtractor.extract_mav(signal_data)
        result = self._loaded_model.predict([mav_features])
        return result


if __name__ == '__main__':
    path_to_knn_model = 'knn_model'
    path_to_test_gesture = 'C:/DATA/MyProject/BigProjects/ProjectHand/hand/arm_prosthesis_raspberry/data/gestures' \
                           '/training/sharp_flexion/2021_04_04_17_44_16.csv'

    test_signal = ClassificationTraining.extract_signal_from_csv(path_to_test_gesture)

    predictor = ClassificationPredictor(path_to_knn_model)
    print(predictor.predict(test_signal))

