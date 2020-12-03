import logging
import time
from queue import Queue

from arm_prosthesis.models.gesture import Gesture
from arm_prosthesis.models.gesture_action import GestureAction
from arm_prosthesis.models.positions import Positions


class HandController:
    # EC:56:23:F3:91:FC - Honor 10 Lite
    # 98:D3:71:F9:7A:02 - HCF97A02
    _logger = logging.getLogger('Main')

    # Id жестов по умолчанию для команд execute by raw и set_positions
    _uuid_set_positions = '39d4dab8-e2b5-4751-9b1c-d09ecff94f30'

    def __init__(self):
        self._set_gesture_queue: 'Queue[Gesture]' = Queue()
        self._logger.info('Hand controller initialized')

    def run(self):
        self._logger.info('Hand controller running')
        while 1:
            self._logger.info('Wait new gesture')
            # if there is a gesture in queue, we start execute it
            gesture: Gesture = self._set_gesture_queue.get()
            self._logger.info('New gesture receive from the queue. Start execute gesture')
            self.gesture_executor(gesture)

    def gesture_executor(self, gesture: Gesture):
        if gesture is None:
            raise TypeError

        action_number = 0
        repeat_counter = 0

        self._logger.info(f'Start execute gesture with uuid - {gesture.uuid} ({gesture.name}).')

        if gesture.actions is None:
            self._logger.error('Gesture actions is none. Mock actions list to empty list.')
            actions_list = []
        else:
            actions_list = gesture.actions

        number_of_actions = len(actions_list)
        self._logger.info(
            f'Count of actions {number_of_actions}. Is iterable gesture - {gesture.iterable}. Number of repetitions -'
            f' {gesture.repetitions}')

        # a repeated gesture can be performed until a new gesture arrives
        while (self._set_gesture_queue.empty() and (gesture.iterable or
               (action_number < number_of_actions and
                repeat_counter < gesture.repetitions))):

            action = actions_list[action_number]
            self._logger.debug(f'Get action with index {action_number}')

            # if all actions in list were completed
            if number_of_actions == action_number + 1:
                action_number = 0
                repeat_counter += 1
                self._logger.debug(f'All actions is done. Repeat counter is {repeat_counter}')
            else:
                action_number += 1

            self._logger.debug(f'Delay {action.delay} ms before next action')
            time.sleep(action.delay / 1000)

    def set_positions(self, positions: Positions):
        self._logger.info('Set positions execute')
        action = GestureAction(positions.little_finger_position, positions.ring_finger_position,
                               positions.middle_finger_position, positions.index_finger_position,
                               positions.thumb_finger_position, positions.thumb_ejector_position, 0)

        actions_list = [action]
        gesture = Gesture(self._uuid_set_positions, "SET_POSITIONS", 0, False, 1, actions_list)

        self._set_gesture_queue.put(gesture)
