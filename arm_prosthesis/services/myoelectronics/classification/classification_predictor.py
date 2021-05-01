import pickle
import logging

from arm_prosthesis.services.myoelectronics.classification.classification_training import ClassificationTraining
from arm_prosthesis.services.myoelectronics.preprocessing.feture_extactor import FeatureExtractor


class ClassificationPredictor:
    _logger = logging.getLogger('Main')

    def __init__(self, path_to_model):
        # load the model from disk
        print('Model loading')

        import time
        start_time = time.time()
        self._loaded_model = pickle.load(open(path_to_model, 'rb'))

        print("--- %s seconds ---" % (time.time() - start_time))
        print('Model loaded')

    def predict(self, signal_data):
        print('Start recognition')
        import time
        start_time = time.time()

        mav_features = FeatureExtractor.extract_mav(signal_data)
        result = self._loaded_model.predict([mav_features])

        print("--- %s seconds ---" % (time.time() - start_time))
        print('End recognition')

        return result


if __name__ == '__main__':
    path_to_knn_model = 'knn_model'
    path_to_test_gesture = '//home/pi/arm-prosthesis/data/gestures/training/clenching/2021_04_04_17_47_28.csv'

    test_signal = ClassificationTraining.extract_signal_from_csv(path_to_test_gesture)

    predictor = ClassificationPredictor(path_to_knn_model)
    print('Result class - ' + str(predictor.predict(test_signal)[0]))

