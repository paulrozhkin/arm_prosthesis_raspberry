import sys
import glob
import time
#import bluetooth
#import serial
import sys
import os
import platform
import random
from threading import Thread
#from bluedot.btcomm import BluetoothClient
#from signal import pause
#import spidev


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

def signal_recognizer(value):
    global signal
    signal = value


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

def SPI_SET_POSITION_REQUEST_MOCK():
    A = 1
    B = random.randint(0, 65535)
    PointerFingerPosition = random.randint(0, 65535)
    MiddleFingerPosition = random.randint(0, 65535)
    RingFinderPosition = random.randint(0, 65535)
    LittleFingerPosition = random.randint(0, 65535)
    ThumbFingerPosition = random.randint(0, 65535)
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
    if spi_request[0] == 0:
        return SPI_TELEMETRY_REQUEST_MOCK()
    else:
        return SPI_SET_POSITION_ANSWER_MOCK()

def recognize_adc(adc_value):
    global signal
    signal = adc_value

def send_to_display(adc_value):
    time.sleep(adc_value/10000000000)

def get_adc_value():
    global adc_value
    adc_value = ADC_MOCK()
    recognize_adc(adc_value)
    print("ADC_VALUE: ", adc_value)

def get_SPI_telemetry():
    global driver_state
    request = SPI_TELEMETRY_REQUEST_MOCK()
    driver_state = SPI_MOCK(request)
    print("TELEMETRY: ", driver_state)

def get_SPI_answer():
    set_position_request = SPI_SET_POSITION_REQUEST_MOCK()
    spi_answer = SPI_MOCK(set_position_request)
    print("SPI_ANSWER: ", spi_answer)

class I2C_thread(Thread):
    def run(self):
        while 1:
            for i in range(1000):
                get_adc_value()
                time.sleep(0.0025)
            send_to_display(adc_value)

class telemetry_thread(Thread):
    def run(self):
        while 1:
            get_SPI_telemetry()
            time.sleep(0.017)

class spi_answer_thread(Thread):
    def run(self):
        while 1:
            get_SPI_answer()
            time.sleep(1)

def threaded():
    I2C_thread().start()
    telemetry_thread().start()
    spi_answer_thread().start()
# EC:56:23:F3:91:FC - Honor 10 Lite
# 98:D3:71:F9:7A:02 - HCF97A02

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    threaded()
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