from orientation import Orientation
from car import Car


class Board:
    def __init__(self, board_line, width=6, height=6):
        if len(board_line) % width != 0 or len(board_line) / width != height:
            raise Exception("Board input " + board_line + " cannot be split into 6 rows")
        board_line = [board_line[i:i + width] for i in range(0, len(board_line), width)]
        self.matrix = board_line
        self.cars = []
        self.create_cars()
        self.rebuild_table(width, height)

    def create_cars(self):
        assert(len(self.matrix) == 6)
        for row_num, row in enumerate(self.matrix):
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
                elif row_num < 4 and self.matrix[row_num][col_num] == self.matrix[row_num + 1][col_num]\
                        == self.matrix[row_num + 2][col_num]:
                    size = 3
                    orientation = Orientation.VERTICAL
                    car = Car(name, x, y, size, orientation)
                    self.cars.append(car)
                elif row_num < 5 and self.matrix[row_num][col_num] == self.matrix[row_num + 1][col_num]:
                    size = 2
                    orientation = Orientation.VERTICAL
                    car = Car(name, x, y, size, orientation)
                    self.cars.append(car)

    def car_name_exists(self, name):
        for car in self.cars:
            if name == car.name:
                return True
        return False

    def rebuild_table(self, width=6, height=6):
        self.matrix = []
        for i in range(width):
            row = []
            for j in range(height):
                row.append(".")
            self.matrix.append(row)
        for car in self.cars:
            if car.orientation == Orientation.HORIZONTAL:
                for i in range(car.size):
                    self.matrix[car.x][car.y + i] = car.name
            elif car.orientation == Orientation.VERTICAL:
                for i in range(car.size):
                    self.matrix[car.x + i][car.y] = car.name


