import sys
import glob
import time
import bluetooth
import serial
import sys
import os
import platform
from bluedot.btcomm import BluetoothClient
from signal import pause
import spidev


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


# EC:56:23:F3:91:FC - Honor 10 Lite
# 98:D3:71:F9:7A:02 - HCF97A02

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # nearby_devices = bluetooth.discover_devices(lookup_names=True)
    # print("Found {} devices.".format(len(nearby_devices)))
    #
    # for addr, name in nearby_devices:
    #     print("  {} - {}".format(addr, name))

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

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
