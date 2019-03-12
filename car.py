from step import Step


class Car:
    def __init__(self, name, x, y, size, orientation):
        self.name = name
        self.x = x
        self.y = y
        self.size = size
        self.orientation = orientation

    # Return a list of steps that a car can take is a specific direction.
    # Here, we mapped every direction problem to checking if a car can move to the right.
    # We did so by reversing the rows for LEFT, transpose the matrix for UP, reverse transpose for DOWN.
    def find_direction_steps(self, board_row, direction, steps):
        count = False
        i = 1
        for col in board_row:
            if col == self.name:
                count = True
            if col != "." and col != self.name and count:
                break
            if col == "." and count:
                step = Step(self.name, direction, i)
                steps.append(step)
                i = i + 1
