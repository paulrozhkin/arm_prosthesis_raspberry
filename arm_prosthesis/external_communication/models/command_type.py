from enum import Enum


class CommandType(Enum):
    Ok = 1
    Error = 2
    Telemetry = 3
    GetSettings = 4
    SetSettings = 5
    GetGestures = 6
    SaveGesture = 7
    DeleteGesture = 8
    PerformGestureId = 9
    PerformGestureRaw = 10
    SetPositions = 11
    UpdateLastTimeSync = 12
    GetTelemetry = 13
    StartTelemetry = 14
    StopTelemetry = 15
    GetMioPatterns = 16
    SetMioPatterns = 17
