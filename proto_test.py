import enums_pb2 as enums
from settings_pb2 import GetSettings, SetSettings
from telemetry_pb2 import Telemetry
from datetime import datetime
from datetime import timezone

def telemetry_test():
    data_telemetry = bytearray.fromhex("08 28 10 01 18 04 20 03 28 04 30 C8 85 AF FD 05 38 01 42 26 0A 24 39 37 66 37 32 64 38 34 2D 62 38 35 36 2D 34 39 33 34 2D 38 64 38 30 2D 32 62 33 66 66 35 61 64 34 31 64 35 48 01 50 02 58 03 60 04 68 05 70 06")

    telemetry_data = Telemetry()
    telemetry_data.ParseFromString(data_telemetry)
    print(telemetry_data)

    telemetry_data.last_time_sync = int(datetime.utcnow().timestamp())
    bytes = telemetry_data.SerializeToString()
    print(''.join('{:02x} '.format(x) for x in bytes))

    telemetry_data = Telemetry()
    telemetry_data.ParseFromString(bytes)
    print(telemetry_data.last_time_sync)


if __name__ == '__main__':
    getSettings = GetSettings()

    telemetry_test()
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
