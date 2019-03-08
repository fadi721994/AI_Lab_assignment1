from board import Board
from direction import Direction
from state import State
from priority_queue import PriorityQueue
from priority_queue_node import PriorityQueueNode
import copy


DATA = None


# Read the boards from rh.txt file and provide a list of object "board"
def parse_list_of_boards(file="rh.txt"):
    list_of_boards = []
    with open(file, 'r') as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            board = Board(line, i)
            list_of_boards.append(board)
    return list_of_boards


# Return the distance of the red car from the exit.
def calculate_exit_distance(state):
    exit_row = state.board.grid[2]
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


def create_expansion(state, step):
    global DATA
    board = copy.deepcopy(state.board)
    new_state = State(board, state, step, 0, state.steps + step.amount)
    car = new_state.board.get_car_by_name(step.car_name)
    if step.direction == Direction.RIGHT:
        car.y = car.y + step.amount
    elif step.direction == Direction.LEFT:
        car.y = car.y - step.amount
    elif step.direction == Direction.DOWN:
        car.x = car.x + step.amount
    elif step.direction == Direction.UP:
        car.x = car.x - step.amount
    new_state.board.build_grid()
    f = new_state.board.calculate_f(new_state.steps, DATA)
    new_state.f_value = f
    return new_state


def expand_state(state):
    list_of_expansions = []
    for car in state.board.cars:
        if state.board.can_car_move(car):
            valid_steps = state.board.find_car_valid_steps(car)
            for step in valid_steps:
                expanded_state = create_expansion(state, step)
                list_of_expansions.append(expanded_state)
    return list_of_expansions


def is_expansion_in_lists(state, open_list, closed_list):
    if PriorityQueueNode(0, state) in open_list.queue:
        return True
    for entry in closed_list:
        if state.board.grid == entry.board.grid:
            return True
    return False


def is_expansion_in_closed_list(state, closed_list):
    for entry in closed_list:
        if state.board.grid == entry.board.grid:
            return True
    return False


def get_solution_steps(state):
    steps = [state.step_taken]
    while state.prev_state is not None:
        steps.append(state.prev_state.step_taken)
        state = state.prev_state
    return steps


def create_solution_string(steps, final_state):
    steps = list(reversed(steps))
    solution_str = ''
    for step in steps:
        if step is not None:
            name = step.car_name
            direction = step.direction
            amount = step.amount
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


def remove_state(state, closed_list):
    for entry in closed_list:
        if state.board.grid == entry.board.grid:
            closed_list.remove(entry)
            break


def grid_to_str(grid):
    grid_line = ''
    for line in grid:
        line = ''.join(line)
        grid_line = grid_line + line
    return grid_line


def solve_board(board, data):
    global DATA
    DATA = data
    steps = 0
    f_values = dict()
    f = board.calculate_f(steps, DATA)
    f_values[hash(grid_to_str(board.grid))] = f
    first_state = State(board, None, None, f, steps)

    open_list = PriorityQueue()
    closed_list = set()

    # Step 1: Put the start node on a list called OPEN of unexpanded nodes.
    # Calculate f(s) and associate its value with node s.
    open_list.push(first_state)
    # Step 2: If OPEN is empty, exit with failure, no solution exists.
    while open_list.is_empty():
        # Step 3: Select from OPEN a node i at which f is minimum. If several nodes qualify,
        # choose a goal node if there is one, otherwise choose among them arbitrarily.
        state = open_list.pop().state

        # Step 4: Remove node i from OPEN and place it on a list called CLOSED, of expanded nodes.
        closed_list.add(state)

        # Step 5: If i is a goal node, exit with success; a solution has been found.
        if state.goal_state():
            solution_steps = get_solution_steps(state)
            solution_str = create_solution_string(solution_steps, state)
            return solution_str

        # Step 6: Expand node i, creating nodes for all of its successors. For every successor node j of i:
        # Step 6.1: Calculate f(j)
        expanded_states = expand_state(state)
        for expanded_state in expanded_states:
            # Step 6.2: If j is neither in OPEN nor in CLOSED, then add it to OPEN with its f value.
            # Attach a pointer from j back to its predecessor i
            if not is_expansion_in_lists(expanded_state, open_list, closed_list):
                open_list.push(expanded_state)
            else:
                # Step 6.3: If j was already on either OPEN or CLOSED, compare the f value just calculated for j with
                # the value previously associated with the node.
                if expanded_state.f_value < f_values[hash(grid_to_str(expanded_state.board.grid))]:
                    # Step 6.3.1: Substitute it for the old value.
                    if is_expansion_in_closed_list(expanded_state, closed_list):
                        # Step 6.3.2: Point j back to i instead of to its previously found predecessor.
                        # Step 6.3.3: If node j was on the CLOSED list, move it back to OPEN
                        open_list.push(expanded_state)
                        remove_state(expanded_state, closed_list)
            f_values[hash(grid_to_str(expanded_state.board.grid))] = expanded_state.f_value
    return None


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
