from resources.DataStructures import Command
from SPI.DriverMotors import get_telemetry

'''
    functional that execute commands from MQTT and just refer to it
'''
def send_telemetry_to_MQTT():
    driver_state = get_telemetry("MQTT")
    print("send_telemetry_to_MQTT", driver_state)

def MQTT_Proxy_command_receive():
    print("MQTT Proxy command was received")
    command = Command("Telemetry", 100)
    return command

def MQTT_Proxy_send_reply(command_name):
    print("send_reply_to_MQTT for command ", command_name)

def send_settings_to_MQTT():
    print ("send_settings_to_MQTT")

def set_settings_from_MQTT(settings):
    print("set_settings_from_MQTT ", settings)

def send_gestures_list_to_MQTT():
    #find list and send
    list = []
    print("send_gestures_list_to_MQTT")

def save_gesture_from_MQTT(gesture):
    print("save_gesture_from_MQTT")

def save_gesture(gesture_list):
    f = open('gesture_list', 'w')
    f.write(gesture_list)

def delete_gesture(gesture):
    print("delete_gesture_from_MQTT")

#find gesture in memory with required id
def find_gesture_by_id(id):
    print("find_gesture_by_id")