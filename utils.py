from board import Board
from orientation import Orientation
from direction import Direction
import copy


DEPTHS = []


# Read the boards from rh.txt file and provide a list of object "board"
def parse_list_of_boards(file="rh.txt"):
    list_of_boards = []
    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            board = Board(line)
            list_of_boards.append(board)
    return list_of_boards


# Return the distance of the red car from the exit.
def calculate_exit_distance(board):
    exit_row = board.matrix[2]
    distance = 0
    count = False
    for col in exit_row:
        if col == "X":
            count = True
        if count and col != "X":
            distance = distance + 1
    return distance


# Print the board in a nicer way
def prettify_print(board):
    print("++++++++")
    for i, row in enumerate(board):
        line = "+"
        for col in row:
            line = line + col
        line = line + "+"
        if i == 2:
            line = line + "#"
        print(line)
    print("++++++++")


# Given a car name and a list of cars, return the relevant car object
def get_car_by_name(name, cars):
    for car in cars:
        if name.lower() == car.name.lower():
            return car
    return None


# Checks if car blocking X, is also blocked.
def is_blocking_car_blocked(board, car):
    if car.size == 3:
        for x, row in enumerate(board[3:]):
            if board[x + 3][car.y] != "." and board[x + 3][car.y] != car.name:
                return True
    elif car.size == 2:
        if (board[0][car.y] != "." and board[0][car.y] != car.name) or \
                (board[1][car.y] != "." and board[1][car.y] != car.name) or \
                (board[3][car.y] != "." and board[3][car.y] != car.name) or \
                (board[4][car.y] != "." and board[4][car.y] != car.name):
            return True
    return False


# Returns the number of cars blocking X if count_blocked is false, if true, returns an extra point for each blocked car
def calculate_blocking_cars(board, count_blocked=True):
    exit_row = board.matrix[2]
    blocking_cars = 0
    count = False
    for col in exit_row:
        if col == "X":
            count = True
        if count and col != "X" and col != ".":
            car = get_car_by_name(col, board.cars)
            if car is None:
                assert 0
            if count_blocked:
                is_blocked = is_blocking_car_blocked(board.matrix, car)
                # if is_blocked:
                #     blocking_cars = blocking_cars + 1
            blocking_cars = blocking_cars + 1
    return blocking_cars


# G is the number of blocking cars
def calculate_g(board):
    blocking_cars_points = calculate_blocking_cars(board)
    return blocking_cars_points


def calculate_f(board, cost):
    return cost + calculate_g(board)


def select_min_state(open_list):
    minimum = open_list[0][1]
    min_list = []
    for i, entry in enumerate(open_list):
        if entry[1] < minimum:
            minimum = entry[1]
    for entry in open_list:
        if entry[1] == minimum:
            min_list.append(entry)
    for entry in min_list:
        if goal_state(entry[0]):
            return entry
    return min_list[0]


def update_lists(list_entry, open_list, closed_list):
    for entry in open_list:
        if list_entry[0].matrix == entry[0].matrix:
            closed_list.append(list_entry)
            open_list.remove(list_entry)


def goal_state(state):
    blocking_cars = calculate_blocking_cars(state, False)
    # Check if goal state
    if blocking_cars == 0:
        return True
    return False


def can_car_move(car, board):
    x = car.x
    y = car.y
    if car.orientation == Orientation.HORIZONTAL:
        if y == 0:
            if board[x][y + car.size] != ".":
                return False
        elif y + car.size == 6:
            if board[x][y - 1] != ".":
                return False
        else:
            if board[x][y - 1] != "." and board[x][y + car.size] != ".":
                return False
    elif car.orientation == Orientation.VERTICAL:
        if x == 0:
            if board[x + car.size][y] != ".":
                return False
        elif x + car.size == 6:
            if board[x - 1][y] != ".":
                return False
        else:
            if board[x - 1][y] != "." and board[x + car.size][y] != ".":
                return False
    return True


# Convert UP, DOWN, LEFT movement problems to RIGHT problem.
def find_direction_steps(car, board_row, direction, steps):
    count = False
    i = 1
    for col in board_row:
        if col == car.name:
            count = True
        if col != "." and col != car.name and count:
            break
        if col == "." and count:
            steps.append((car.name, direction, i))
            i = i + 1


def find_car_valid_steps(car, board):
    steps = []
    x = car.x
    y = car.y
    if car.orientation == Orientation.HORIZONTAL:
        row = board[x]
        reversed_row = list(reversed(board[x]))
        # Find right steps:
        find_direction_steps(car, row, Direction.RIGHT, steps)
        # Find left steps:
        find_direction_steps(car, reversed_row, Direction.LEFT, steps)
        return steps
    if car.orientation == Orientation.VERTICAL:
        transpose_board = [list(i) for i in zip(*board)]
        col = transpose_board[y]
        reversed_col = list(reversed(transpose_board[y]))
        # Find right steps:
        find_direction_steps(car, col, Direction.DOWN, steps)
        # Find left steps:
        find_direction_steps(car, reversed_col, Direction.UP, steps)
        return steps


def create_expansion(state, step):
    new_state = copy.deepcopy(state)
    car = get_car_by_name(step[0], new_state.cars)
    if step[1] == Direction.RIGHT:
        car.y = car.y + step[2]
    elif step[1] == Direction.LEFT:
        car.y = car.y - step[2]
    elif step[1] == Direction.DOWN:
        car.x = car.x + step[2]
    elif step[1] == Direction.UP:
        car.x = car.x - step[2]
    new_state.rebuild_table()
    return new_state


def expand_state(state, cost, depth):
    list_of_expansions = []
    for car in state.cars:
        if can_car_move(car, state.matrix):
            valid_steps = find_car_valid_steps(car, state.matrix)
            for step in valid_steps:
                expanded_state = create_expansion(state, step)
                f = calculate_f(expanded_state, cost + step[2])
                list_of_expansions.append((expanded_state, f, state, step, cost + step[2], depth + 1))
    return list_of_expansions


def is_expansion_in_lists(expansion, open_list, closed_list):
    for entry in open_list:
        if expansion[0].matrix == entry[0].matrix:
            return True
    for entry in closed_list:
        if expansion[0].matrix == entry[0].matrix:
            return True
    return False


def find_path(list_entry, closed_list, steps, done, depth=1):
    for entry in closed_list:
        if list_entry[2] is None:
            DEPTHS.append(depth)
            done = True
        if done:
            return done
        if list_entry[2].matrix == entry[0].matrix:
            if entry[3] is not None:
                steps.append(entry[3])
            done = find_path(entry, closed_list, steps, done, depth + 1)
    return done


def get_path_string(steps, final_state):
    steps = list(reversed(steps))
    solution_str = ''
    for step in steps:
        name = step[0]
        direction = step[1]
        amount = step[2]
        direction_letter = ''
        if direction == Direction.DOWN:
            direction_letter = 'D'
        elif direction == Direction.UP:
            direction_letter = 'U'
        elif direction == Direction.LEFT:
            direction_letter = 'L'
        elif direction == Direction.RIGHT:
            direction_letter = 'R'
        solution_str = solution_str + name + direction_letter + str(amount) + ' '
    exit_dist = calculate_exit_distance(final_state)
    solution_str = solution_str + 'XR' + str(exit_dist + 2)
    return solution_str.strip()


def solve_board(state):
    del DEPTHS[:]
    cost = 0
    max_depth = 0
    f = calculate_f(state, cost)
    # state, F, prev_state, step, cost, depth
    open_list = [(state, f, None, None, cost, 1)]
    closed_list = []

    while True:
        if len(open_list) == 0:
            return None
        open_list_entry = select_min_state(open_list)
        update_lists(open_list_entry, open_list, closed_list)
        next_state = open_list_entry[0]
        cost = open_list_entry[4]
        depth = open_list_entry[5]
        if goal_state(next_state):
            steps = [open_list_entry[3]]
            find_path(open_list_entry, closed_list, steps, False)
            path_str = get_path_string(steps, next_state)
            print("Max depth is " + str(max_depth))
            return path_str
        list_of_expansions = expand_state(next_state, cost, depth)
        for expansion in list_of_expansions:
            if not is_expansion_in_lists(expansion, open_list, closed_list):
                if depth > max_depth:
                    max_depth = depth
                open_list.append(expansion)


def count_steps(sol):
    step_sum = 0
    for c in sol:
        if c.isdigit():
            step_sum += int(c)
    return step_sum


def validate_solution(real_sol, my_sol):
    real_steps = count_steps(real_sol)
    my_steps = count_steps(my_sol)
    if real_steps > my_steps:
        return 1
        print("Too optimal. Our steps were " + str(my_steps) + " while solution was " + str(real_steps))
    elif real_steps < my_steps:
        return -1
        print("Not optimal. Our steps were " + str(my_steps) + " while solution was " + str(real_steps))
    else:
        return 0
        print("Optimal. Our steps were " + str(my_steps) + " while solution was " + str(real_steps))


def read_solutions():
    solutions = []
    with open("given_solutions.txt", 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            solutions.append(line)
    return solutions
