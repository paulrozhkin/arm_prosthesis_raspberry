import sys
import glob
import time
#import bluetooth
#import serial
import sys
import os
import platform
import random
from datetime import datetime
from threading import Thread
from queue import Queue
#from bluedot.btcomm import BluetoothClient
#from signal import pause
#import spidev

def save_gesture(gesture_list):
    f = open('gesture_list', 'w')
    f.write(gesture_list)

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def data_received(data):
    print(data)

class Command(object):
    def __init__(self, Name, Payload):
        self.Name = Name
        self.Payload = Payload

class Gesture(object):
    def __init__(self, ID, NAME, LastTimeSync,
                 IterableGesture, NumberOfGestureRepetitions,
                 NumberOfMotions, ListActions):
        self.ID = ID
        self.NAME = NAME
        self.LastTimeSync = LastTimeSync
        self.IterableGesture = IterableGesture
        self.NumberOfGestureRepetitions = NumberOfGestureRepetitions
        self.NumberOfMotions = NumberOfMotions
        self.ListActions = ListActions

class GestureAction(object):
    def __init__(self, PointerFingerPosition, MiddleFingerPosition, RingFinderPosition,
                 LittleFingerPosition, ThumbFingerPosition, Delay):
        self.PointerFingerPosition = PointerFingerPosition
        self.MiddleFingerPosition = MiddleFingerPosition
        self.RingFinderPosition = RingFinderPosition
        self.LittleFingerPosition = LittleFingerPosition
        self.ThumbFingerPosition = ThumbFingerPosition
        self.Delay = Delay

def MQTT_Proxy_command_receive():
    print("MQTT Proxy command was received")
    command = Command("Telemetry", 100)
    return command

def MQTT_Proxy_telemetry_send():
    print ("send telemetry to MQTT")

def ADC_MOCK():
    return random.randint(0, 65535)

def SPI_TELEMETRY_REQUEST_MOCK():
    A = 0
    B = random.randint(0, 65535)
    C = random.randint(0, 65535)
    D = random.randint(0, 65535)
    E = random.randint(0, 65535)
    F = random.randint(0, 65535)
    G = random.randint(0, 65535)
    CRC8 = random.randint(0, 65535)
    I = random.randint(0, 65535)
    J = random.randint(0, 65535)
    K = random.randint(0, 65535)
    L = random.randint(0, 65535)
    M = random.randint(0, 65535)
    N = random.randint(0, 65535)
    O = random.randint(0, 65535)
    P = random.randint(0, 65535)

    telemetry_request = [A, B, C, D, E, F, G, CRC8, I, J, K, L, M, N, O, P]
    return telemetry_request

def SPI_SET_POSITION_REQUEST(action):
    A = 1
    B = random.randint(0, 65535)
    PointerFingerPosition = action.PointerFingerPosition    #random.randint(0, 65535)
    MiddleFingerPosition = action.MiddleFingerPosition  #random.randint(0, 65535)
    RingFinderPosition = action.RingFinderPosition  #random.randint(0, 65535)
    LittleFingerPosition = action.LittleFingerPosition  #random.randint(0, 65535)
    ThumbFingerPosition = action.ThumbFingerPosition    #random.randint(0, 65535)
    CRC8 = random.randint(0, 65535)
    I = random.randint(0, 65535)
    G = random.randint(0, 65535)
    K = random.randint(0, 65535)
    L = random.randint(0, 65535)
    M = random.randint(0, 65535)
    N = random.randint(0, 65535)
    O = random.randint(0, 65535)
    P = random.randint(0, 65535)
    request = [A, B, PointerFingerPosition, MiddleFingerPosition, RingFinderPosition,
               LittleFingerPosition, ThumbFingerPosition, CRC8, I, G, K, L, M, N, O, P]
    return request

def SPI_SET_POSITION_ANSWER_MOCK():
    A = random.randint(0, 65535)
    B = random.randint(0, 65535)
    C = random.randint(0, 65535)
    D = random.randint(0, 65535)
    E = random.randint(0, 65535)
    F = random.randint(0, 65535)
    G = random.randint(0, 65535)
    H = random.randint(0, 65535)
    I = 1
    CurrentRegime = random.randint(0, 3)
    PointerFingerPosition = random.randint(0, 65535)
    MiddleFingerPosition = random.randint(0, 65535)
    RingFinderPosition = random.randint(0, 65535)
    LittleFingerPosition = random.randint(0, 65535)
    ThumbFingerPosition = random.randint(0, 65535)
    CRC8 = random.randint(0, 65535)

    answer = [A, B, C, D, E, F, G, H, I, CurrentRegime,
               PointerFingerPosition, MiddleFingerPosition, RingFinderPosition,
               LittleFingerPosition, ThumbFingerPosition, CRC8]
    return answer

def SPI_MOCK(spi_request):
    print(spi_request[0])
    if spi_request[0] == 0:
        return SPI_TELEMETRY_REQUEST_MOCK()
    else:
        return SPI_SET_POSITION_ANSWER_MOCK()

def recognize_adc(adc_value):
    global signal
    signal = round(adc_value*3/65536, 2)
    print("VOLT: "+str(signal))
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

def send_to_display(adc_value):
    display_command = [adc_value, 0xFFFF, 0xFFFF]
    print("display : ", display_command)

def get_adc_value():
    global adc_value
    adc_value = ADC_MOCK()
    print("ADC_VALUE: ", adc_value)

def get_SPI_telemetry():
    global driver_state
    request = SPI_TELEMETRY_REQUEST_MOCK()
    driver_state = SPI_MOCK(request)
    print("TELEMETRY: ", driver_state)

def get_SPI_answer():
    set_position_request = SPI_SET_POSITION_REQUEST(GestureAction(0,0,0,0,0,0))
    spi_answer = SPI_MOCK(set_position_request)
    print("SPI_ANSWER: ", spi_answer)

def SPI_send_set_position_request(action):
    request = SPI_SET_POSITION_REQUEST(action)
    print("Set Pos Request: ", request)

def send_telemetry_to_MQTT(driver_state):
    print("send_telemetry_to_MQTT", driver_state)

def MQTT_Proxy_send_answer(command_name):
    print("send_reply_to_MQTT for command ", command_name)

def send_settings_to_MQTT():
    print ("send_settings_to_MQTT")

def set_settings_from_MQTT(settings):
    print("set_settings_from_MQTT")

def send_gestures_list_to_MQTT():
    #достать список и отправить
    list = [current_gesture]
    print("send_gestures_list_to_MQTT")

def save_gesture_from_MQTT(gesture):
    print("save_gesture_from_MQTT")

def delete_gesture_from_MQTT(gesture):
    print("delete_gesture_from_MQTT")

def find_gesture_by_id(id):
    print("find_gesture_by_id")

class I2C_thread(Thread):
    def run(self):
        display_time = time.time()
        while 1:
            get_adc_value()
            time.sleep(0.005)
            now = time.time()
            if now - display_time > 0.15:
                display_time = now
                send_to_display(adc_value)

class SPI_telemetry_thread(Thread):
    def run(self):
        while 1:
            get_SPI_telemetry()
            time.sleep(0.017)

class SPI_answer_thread(Thread):
    def run(self):
        while 1:
            get_SPI_answer()
            time.sleep(1)

class adc_recognizer_thread(Thread):
    def run(self):
        while 1:
            recognize_adc(adc_value)
            time.sleep(0.005)

class SPI_set_position_thread(Thread):
    cur = Gesture
    def run(self):
        while 1:
            cur_gest = set_position_queue.get()
            # если есть запрос, то отправляем, иначе скипаем.
            if cur_gest:
                print("we are sending set position requests")
                action_number = -1
                repeat_counter = 0
                #жест может повторяться... по какому событию он прекращает повторяться?
                while cur_gest.IterableGesture or action_number < cur_gest.NumberOfMotions \
                        and repeat_counter < cur_gest.NumberOfGestureRepetitions:
                    action_number += 1
                    action = cur_gest.ListActions[action_number]
                    SPI_send_set_position_request(action)
                    if (cur_gest.NumberOfMotions == action_number + 1):
                        action_number = 0
                        repeat_counter += 1
                    print("Cur Delay ", action.Delay)
                    time.sleep(action.Delay)
                print("End of gesture execution")

class MQTT_commands_executor_thread(Thread):
    def run(self):
        global frequency
        frequency = 1
        while 1:
            #always send telemetry
            send_telemetry_to_MQTT(driver_state)
            time.sleep(1/frequency)
            # sometimes exec commands
            command = MQTT_command_queue.get()
            if command:
                if command.Name == "Telemetry":
                    frequency = random.randint(1, 200)
                elif command.Name == "GetSettings":
                    send_settings_to_MQTT()
                elif command.Name == "SetSettings":
                    settings = command.Payload
                    set_settings_from_MQTT(settings)
                elif command.Name == "GetGestures":
                    send_gestures_list_to_MQTT()
                elif command.Name == "SaveGesture":
                    gesture = command.Payload
                    save_gesture_from_MQTT(gesture)
                elif command.Name == "DeleteGesture":
                    gesture = command.Payload
                    delete_gesture_from_MQTT(gesture)
                elif command.Name == "PerformGestureId":
                    id = command.Payload
                    gesture = find_gesture_by_id(id)
                    # нужна приоритетная очередь для жестов?
                    if gesture != None:
                        gesture_queue.put(gesture)
                elif command.Name == "PerformGestureRaw":
                    gesture = command.Payload
                    gesture_queue.put(gesture)

def threaded():
    I2C_thread().start()
    adc_recognizer_thread().start()
    SPI_telemetry_thread().start()
    SPI_answer_thread().start()
    SPI_set_position_thread().start()
    MQTT_commands_executor_thread().start()

# EC:56:23:F3:91:FC - Honor 10 Lite
# 98:D3:71:F9:7A:02 - HCF97A02

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    set_position_queue = Queue()
    gesture_queue = Queue()
    MQTT_command_queue = Queue()

    global current_gesture
    global mode
    mode = 2 #AUTO

    threaded()

    while(1):
        gesture = gesture_queue.get()
        if gesture:
            print("Have a gesture for execution")
            set_position_queue.put(gesture)

        command = MQTT_Proxy_command_receive()
        if command:
            MQTT_command_queue.put(command)

        #MQTT_Proxy_send_answer(command.name)

    #main()

    # nearby_devices = bluetooth.discover_devices(lookup_names=True)
    # print("Found {} devices.".format(len(nearby_devices)))
    #
    # for addr, name in nearby_devices:
    #     print("  {} - {}".format(addr, name))

'''
    # Передача на MQTT Proxy
    c = BluetoothClient("98:D3:71:F9:7A:02", data_received)
    c.send("ON")
    c.disconnect()

    # Передача на драйвер моторов
    spi = spidev.SpiDev()
    spi.open(0, 0)

    spi.bits_per_word = 8
    spi.max_speed_hz = 500000

    # send command to spi
    spi.xfer([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    # receive telemetry
    result = spi.xfer([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
    print(result)
    # spi.writebytes([])

    spi.close()

    # pause()

    # print(serial_ports())
    # print("Start connect")
    # ser = serial.Serial('/dev/ttyprintk')
    # print(ser.name)
    # time.sleep(10)
    # ser.close()
    # print("End")
'''