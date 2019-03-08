from utils import *
from data import Data
from heuristic import Heuristic


def main():
    heuristics = [Heuristic.BLOCKING_CARS, Heuristic.BLOCKED_BLOCKING_CARS]
    list_of_boards = parse_list_of_boards()
    list_of_solutions = read_solutions()
    for heuristic in heuristics:
        if heuristic == Heuristic.BLOCKED_BLOCKING_CARS:
            break
        for i, board in enumerate(list_of_boards):
            data = Data(i, heuristic)
            solution = solve_board(board, data)

            if solution is None:
                print("No solution was found")
            else:
                val = validate_solution(list_of_solutions[i], solution)
                if val == 1:
                    print("Too optimal")
                elif val == 0:
                    print("Optimal")
                elif val == -1:
                    print("Not optimal")
                print(solution)


main()
