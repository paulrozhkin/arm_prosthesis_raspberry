import glob
import time
#import bluetooth
#import serial
import sys
from threading import Thread
from queue import Queue
#from bluedot.btcomm import BluetoothClient
#from signal import pause
#import spidev

from I2C.EMG_ADC import *
from I2C.Display import *
from SPI.DriverMotors import *
from mqtt import *
from resources.DataStructures import *

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

#this thread serves I2C devices like ADC, Display, Accelerometer
class I2C_thread(Thread):
    def run(self):
        display_time = time.time()
        while 1:
            get_adc_value()
            time.sleep(0.005)
            now = time.time() 
            if now - display_time > 0.15:
                display_time = now
                send_to_display()

#this thread performs analysis of readings from the EMG-sensor after ADC
class adc_recognizer_thread(Thread):
    def run(self):
        while 1:
            # the gesture_queue has nothing to do with it logically
            recognize_adc(gesture_queue)
            time.sleep(0.005)

#this thread serves telemetry receiving from Driver Motors via SPI connection
class SPI_telemetry_thread(Thread):
    def run(self):
        while 1:
            get_telemetry("SPI")
            time.sleep(0.017)

#this thread serves answers from Driver Motors via SPI connection
class SPI_answer_thread(Thread):
    def run(self):
        while 1:
            get_SPI_answer()
            time.sleep(1)

#this thread serves the execution of gestures (sending positions to the Driver Motors via SPI connection)
class SPI_set_position_thread(Thread):
    cur = Gesture
    def run(self):
        global interrupt
        interrupt = 0
        while 1:
            cur_gest = set_position_queue.get()
            # if there is a gesture in queue, we start execute it, otherwise skip it
            if cur_gest:
                print("we are sending set position requests")
                action_number = -1
                repeat_counter = 0
                # a repeated gesture can be performed until a new gesture arrives
                while ((cur_gest.IterableGesture and not set_position_queue.empty()) or
                        (action_number < cur_gest.NumberOfMotions and
                         repeat_counter < cur_gest.NumberOfGestureRepetitions)) and interrupt == 0:
                    action_number += 1
                    action = cur_gest.ListActions[action_number]
                    SPI_send_set_position_request(action)
                    # if all actions in list were completed
                    if (cur_gest.NumberOfMotions == action_number + 1):
                        action_number = 0
                        repeat_counter += 1
                    print("Cur Delay ", action.Delay)
                    time.sleep(action.Delay)
                print("Interrupt", interrupt)
                interrupt = 0
                print("End of gesture execution")


#this thread serves execution of commands that came via MQTT Proxy
class MQTT_commands_executor_thread(Thread):
    def run(self):
        global interrupt
        global frequency
        frequency = 1
        while 1:
            #always send telemetry
            send_telemetry_to_MQTT()
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
                    delete_gesture(gesture)
                elif command.Name == "PerformGestureId":
                    id = command.Payload
                    gesture = find_gesture_by_id(id)
                    # we need a priority queue (gesture_queue) to perform the gesture from MQTT immediately
                    if gesture != None:
                        gesture_queue.put(gesture)
                        interrupt = 1
                elif command.Name == "PerformGestureRaw":
                    gestures = []
                    gestures = command.Payload
                    for gest in gestures:
                        gesture_queue.put(gest)

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
    # queues for different tasks
    set_position_queue = Queue()
    gesture_queue = Queue()
    MQTT_command_queue = Queue()

    global current_gesture
    global mode
    mode = 2 #AUTO
    # value to stop execute low priority gesture
    global interrupt

    #run multithreading
    threaded()

    # main thread is used for starting gestures executions and receiving commands from MQTT Proxy
    while(1):
        # check gesture for execution in the queue
        gesture = gesture_queue.get()
        if gesture:
            print("Have a gesture for execution")
            set_position_queue.put(gesture)

        # moving a command to the performer thread
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