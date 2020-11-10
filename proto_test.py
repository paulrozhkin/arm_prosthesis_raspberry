import enums_pb2 as enums
from settings_pb2 import GetSettings, SetSettings
from telemetry_pb2 import Telemetry

if __name__ == '__main__':
    getSettings = GetSettings()

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

    #testData = bytearray([0x08, 0x01, 0x10, 0x01, 0x18, 0x00, 0x20, 0x00, 0x28, 0x00, 0x30, 0x00, 0x38, 0x00])

    #testDataDes = SetSettings()
    #testDataDes.ParseFromString(testData)
    #print(testDataDes)

    telemetry = Telemetry()
    telemetry.last_time_sync.GetCurrentTime()
    # print(telemetry.last_time_sync)
