import random
from resources.DataStructures import GestureAction, Gesture
from resources.Mocks import ADC_MOCK

global volt_adc
global adc_value

''' 
    processing information from the EMG-sensor
'''
def get_adc_value():
    global adc_value
    adc_value = ADC_MOCK()
    print("ADC_VALUE: ", adc_value)

def recognize_adc(gesture_queue):
    volt_adc = round(adc_value*3/65536, 2)
    print("VOLT: "+str(volt_adc))
    #уведомить поток gesture executor (main)
    #тут выбрать жест из памяти или ...
    rec = random.randint(1, 100)
    if rec > 50:
        ListActions = []
        Action1 = GestureAction(2, 4, 8, 16, 32, 0.5)
        Action2 = GestureAction(128, 64, 32, 16, 8, 1)
        ListActions.append(Action1)
        ListActions.append(Action2)
        gesture = Gesture(1, "Test Gesture", 0, 0, 1, 2, ListActions)
        print("send gesture in the Queue of gestures")
        gesture_queue.put(gesture)