from orientation import Orientation
from direction import Direction
from car import Car
from heuristic import Heuristic


class Board:
    def __init__(self, board_line, width=6, height=6):
        if len(board_line) % width != 0 or len(board_line) / width != height:
            raise Exception("Board input " + board_line + " cannot be split into 6 rows")
        board_line = [board_line[i:i + width] for i in range(0, len(board_line), width)]
        self.grid = board_line
        self.cars = []
        self.create_cars()
        self.build_grid(width, height)

    # Read the grid lines and create car objects and add them to list.
    def create_cars(self):
        assert(len(self.grid) == 6)
        for row_num, row in enumerate(self.grid):
            for col_num, col in enumerate(row):
                if col == ".":
                    continue
                name = row[col_num]
                x = row_num
                y = col_num
                if self.car_name_exists(name):
                    continue
                if col_num < 4 and row[col_num] == row[col_num + 1] == row[col_num + 2]:
                    size = 3
                    orientation = Orientation.HORIZONTAL
                    car = Car(name, x, y, size, orientation)
                    self.cars.append(car)
                elif col_num < 5 and row[col_num] == row[col_num + 1]:
                    size = 2
                    orientation = Orientation.HORIZONTAL
                    car = Car(name, x, y, size, orientation)
                    self.cars.append(car)
                elif row_num < 4 and self.grid[row_num][col_num] == self.grid[row_num + 1][col_num]\
                        == self.grid[row_num + 2][col_num]:
                    size = 3
                    orientation = Orientation.VERTICAL
                    car = Car(name, x, y, size, orientation)
                    self.cars.append(car)
                elif row_num < 5 and self.grid[row_num][col_num] == self.grid[row_num + 1][col_num]:
                    size = 2
                    orientation = Orientation.VERTICAL
                    car = Car(name, x, y, size, orientation)
                    self.cars.append(car)

    # Check if a car exists on the board using its name
    def car_name_exists(self, name):
        for car in self.cars:
            if name == car.name:
                return True
        return False

    # Build the grid using where the cars are placed.
    def build_grid(self, width=6, height=6):
        self.grid = []
        for i in range(width):
            row = []
            for j in range(height):
                row.append(".")
            self.grid.append(row)
        for car in self.cars:
            if car.orientation == Orientation.HORIZONTAL:
                for i in range(car.size):
                    self.grid[car.x][car.y + i] = car.name
            elif car.orientation == Orientation.VERTICAL:
                for i in range(car.size):
                    self.grid[car.x + i][car.y] = car.name

    # Return a car object when queried with a car name
    def get_car_by_name(self, car_name):
        for car in self.cars:
            if car_name.lower() == car.name.lower():
                return car
        return None

    # Calculate the number of cars blocking X. If count_blocked is True, we add 1 for each blocking car that is blocked.
    def calculate_blocking_cars(self, count_blocked=False):
        exit_row = self.grid[2]
        blocking_cars = 0
        count = False
        for col in exit_row:
            if col == "X":
                count = True
            if count and col != "X" and col != ".":
                car = self.get_car_by_name(col)
                if car is None:
                    assert 0
                if count_blocked:
                    is_blocked = self.is_blocking_car_blocked(car)
                    if is_blocked:
                        blocking_cars = blocking_cars + 1
                blocking_cars = blocking_cars + 1
        return blocking_cars

    # Check if a car that is blocking X, is also blocked.
    def is_blocking_car_blocked(self, car):
        if car.size == 3:
            for x, row in enumerate(self.grid[3:]):
                if self.grid[x + 3][car.y] != "." and self.grid[x + 3][car.y] != car.name:
                    return True
        elif car.size == 2:
            if (self.grid[0][car.y] != "." and self.grid[0][car.y] != car.name) or \
                    (self.grid[1][car.y] != "." and self.grid[1][car.y] != car.name) or \
                    (self.grid[3][car.y] != "." and self.grid[3][car.y] != car.name) or \
                    (self.grid[4][car.y] != "." and self.grid[4][car.y] != car.name):
                return True
        return False

    # Calculate the heuristic function and return its value.
    # Parameter "calc_blocked_blocking", if true, we add 1 for each X-blocking car that is also blocked.
    def calculate_h(self, calc_blocked_blocking):
        blocking_cars_points = self.calculate_blocking_cars(calc_blocked_blocking)
        return blocking_cars_points

    # Calculate the f function.
    def calculate_f(self, steps, data):
        h_value = self.calculate_h(data.heuristic == Heuristic.BLOCKED_BLOCKING_CARS)
        data.heuristic_values.append(h_value)
        return steps + h_value

    # Check if a car can move.
    def can_car_move(self, car):
        x = car.x
        y = car.y
        if car.orientation == Orientation.HORIZONTAL:
            if y == 0:
                if self.grid[x][y + car.size] != ".":
                    return False
            elif y + car.size == 6:
                if self.grid[x][y - 1] != ".":
                    return False
            else:
                if self.grid[x][y - 1] != "." and self.grid[x][y + car.size] != ".":
                    return False
        elif car.orientation == Orientation.VERTICAL:
            if x == 0:
                if self.grid[x + car.size][y] != ".":
                    return False
            elif x + car.size == 6:
                if self.grid[x - 1][y] != ".":
                    return False
            else:
                if self.grid[x - 1][y] != "." and self.grid[x + car.size][y] != ".":
                    return False
        return True

    # Given a car object, return a list of all the possible steps it can take. A step is an object.
    def find_car_valid_steps(self, car):
        steps = []
        x = car.x
        y = car.y
        if car.orientation == Orientation.HORIZONTAL:
            row = self.grid[x]
            reversed_row = list(reversed(self.grid[x]))
            # Find right steps:
            car.find_direction_steps(row, Direction.RIGHT, steps)
            # Find left steps:
            car.find_direction_steps(reversed_row, Direction.LEFT, steps)
            return steps
        if car.orientation == Orientation.VERTICAL:
            transpose_grid = [list(i) for i in zip(*self.grid)]
            col = transpose_grid[y]
            reversed_col = list(reversed(transpose_grid[y]))
            # Find right steps:
            car.find_direction_steps(col, Direction.DOWN, steps)
            # Find left steps:
            car.find_direction_steps(reversed_col, Direction.UP, steps)
            return steps
