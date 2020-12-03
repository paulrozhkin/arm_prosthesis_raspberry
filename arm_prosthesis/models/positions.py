class Positions:
    def __init__(self, little_finger_position: int,
                 ring_finger_position: int,
                 middle_finger_position: int,
                 index_finger_position: int,
                 thumb_finger_position: int,
                 thumb_ejector_position: int = 0):
        self._thumb_finger_position = thumb_finger_position
        self._index_finger_position = index_finger_position
        self._middle_finger_position = middle_finger_position
        self._ring_finger_position = ring_finger_position
        self._little_finger_position = little_finger_position
        self._thumb_ejector_position = thumb_ejector_position

    @property
    def little_finger_position(self) -> int:
        return self._little_finger_position

    @property
    def ring_finger_position(self) -> int:
        return self._ring_finger_position

    @property
    def middle_finger_position(self) -> int:
        return self._middle_finger_position

    @property
    def index_finger_position(self) -> int:
        return self._index_finger_position

    @property
    def thumb_finger_position(self) -> int:
        return self._thumb_finger_position

    @property
    def thumb_ejector_position(self) -> int:
        return self._thumb_ejector_position
