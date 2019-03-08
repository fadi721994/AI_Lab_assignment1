import copy
from direction import Direction


class State:
    def __init__(self, board, prev_state, step_taken, f_value, steps):
        self.board = board
        self.f_value = f_value
        self.prev_state = prev_state
        self.steps = steps
        self.step_taken = step_taken

    def goal_state(self):
        blocking_cars = self.board.calculate_blocking_cars()
        # Check if goal state
        if blocking_cars == 0:
            return True
        return False
