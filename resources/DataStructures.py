'''
    data structures that used executive architecture
'''
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