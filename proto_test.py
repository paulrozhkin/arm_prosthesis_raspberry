import enums_pb2 as enums
from gestures_pb2 import Gesture, GetGestures, GestureAction
from settings_pb2 import GetSettings, SetSettings
from telemetry_pb2 import Telemetry
from datetime import datetime
from datetime import timezone

from uuid_pb2 import UUID as IdArm
import json


def telemetry_test():
    data_telemetry = bytearray.fromhex("08 28 10 01 18 04 20 03 28 04 30 C8 85 AF FD 05 38 01 42 26 0A 24 39 37 66 37 32 64 38 34 2D 62 38 35 36 2D 34 39 33 34 2D 38 64 38 30 2D 32 62 33 66 66 35 61 64 34 31 64 35 48 01 50 02 58 03 60 04 68 05 70 06")

    telemetry_data = Telemetry()
    telemetry_data.ParseFromString(data_telemetry)
    #print(telemetry_data)

    telemetry_data.last_time_sync = int(datetime.utcnow().timestamp())
    bytes = telemetry_data.SerializeToString()
    #print(''.join('{:02x} '.format(x) for x in bytes))

    telemetry_data = Telemetry()
    telemetry_data.pointer_finger_position = 3
    telemetry_data.display_status = enums.MODULE_STATUS_WORK
    bytes = telemetry_data.SerializeToString()
    print(''.join('{:02x} '.format(x) for x in bytes))
    print(telemetry_data.middle_finger_position)


def gesture_test():
    gestures_get = GetGestures()
    gestures_get.last_time_sync = int(datetime.utcnow().timestamp())

    gesture1 = get_gesture()
    gesture1.id.value = "1"
    gesture2 = get_gesture()
    gesture2.id.value = "2"

    gestures_get.gestures.append(gesture1)
    gestures_get.gestures.append(gesture2)

    print(gestures_get)

    bytes_get_gestures = gestures_get.SerializeToString()
    print(''.join('{:02x} '.format(x) for x in bytes_get_gestures))

    gestures_get_des = GetGestures()
    gestures_get_des.ParseFromString(bytes_get_gestures)
    print(gestures_get_des)


def get_gesture():
    gesture = Gesture()
    gesture.id.value = "uuid_gesture"
    gesture.name = "name_gesture"
    gesture.last_time_sync = 155
    gesture.iterable = True
    gesture.repetitions = 6

    action1 = GestureAction()
    action1.pointer_finger_position = 1
    action1.middle_finger_position = 1
    action1.ring_finger_position = 1
    action1.little_finger_position = 1
    action1.thumb_finger_position = 1
    action1.delay = 1

    action2 = GestureAction()
    action2.pointer_finger_position = 2
    action2.middle_finger_position = 2
    action2.ring_finger_position = 2
    action2.little_finger_position = 2
    action2.thumb_finger_position = 2
    action2.delay = 1

    gesture.actions.append(action1)
    gesture.actions.append(action2)

    return gesture


if __name__ == '__main__':
    getSettings = GetSettings()

    gesture_test()
    exit()

    getSettings.enable_emg = True
    getSettings.enable_display = True
    getSettings.enable_driver = True
    getSettings.enable_gyro = True
    getSettings.type_work = enums.MODE_AUTO

    data = getSettings.SerializeToString()

    getSettingsDes = GetSettings()
    getSettingsDes.ParseFromString(data)
    getSettingsDes.enable_display = False

    # print(getSettings)
    # print(getSettingsDes)

    setSettings = SetSettings()
    setSettings.telemetry_frequency = 1
    setSettings.enable_emg = True
    setSettings.enable_display = True
    setSettings.enable_driver = True
    setSettings.enable_gyro = True
    setSettings.type_work = enums.MODE_COMMANDS
    data = setSettings.SerializeToString()
    print(data)

    # testData = bytearray([0x08, 0x01, 0x10, 0x01, 0x18, 0x00, 0x20, 0x00, 0x28, 0x00, 0x30, 0x00, 0x38, 0x00])

    # testDataDes = SetSettings()
    # testDataDes.ParseFromString(testData)
    # print(testDataDes)

    telemetry = Telemetry()
    telemetry.last_time_sync.GetCurrentTime()
    # print(telemetry.last_time_sync)
