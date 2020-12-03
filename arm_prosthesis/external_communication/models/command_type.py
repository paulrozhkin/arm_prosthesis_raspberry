from enum import Enum


class CommandType(Enum):
    Telemetry = 0
    GetSettings = 1
    SetSettings = 2
    GetGestures = 3
    SaveGesture = 4
    DeleteGesture = 5
    PerformGestureId = 6
    PerformGestureRaw = 7
    SetPositions = 8
    Ok = 9
    Error = 10

