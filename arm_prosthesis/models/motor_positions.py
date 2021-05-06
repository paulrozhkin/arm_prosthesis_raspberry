class MotorPositions:
    def __init__(self, little_finger_angle_position, ring_finger_angle_position, middle_finger_angle_position,
                 index_finger_angle_position, thumb_finger_angle_position, thumb_ejector_angle_position):
        self._little_finger_angle_position = little_finger_angle_position
        self._ring_finger_angle_position = ring_finger_angle_position
        self._middle_finger_angle_position = middle_finger_angle_position
        self._index_finger_angle_position = index_finger_angle_position
        self._thumb_finger_angle_position = thumb_finger_angle_position
        self._thumb_ejector_angle_position = thumb_ejector_angle_position

    @property
    def little_finger_angle_position(self) -> int:
        return self._little_finger_angle_position

    @property
    def ring_finger_angle_position(self) -> int:
        return self._ring_finger_angle_position

    @property
    def middle_finger_angle_position(self) -> int:
        return self._middle_finger_angle_position

    @property
    def index_finger_angle_position(self) -> int:
        return self._index_finger_angle_position

    @property
    def thumb_finger_angle_position(self) -> int:
        return self._thumb_finger_angle_position

    @property
    def thumb_ejector_angle_position(self) -> int:
        return self._thumb_ejector_angle_position
