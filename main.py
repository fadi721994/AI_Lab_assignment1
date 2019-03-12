from utils import *
from data import Data
from heuristic import Heuristic
from overall_data import OverallData
import sys
import os


def get_time_limit():
    if len(sys.argv) >= 2:
        time_limit = float(sys.argv[1])
    else:
        time_limit = 25
    return time_limit


def delete_existing_files():
    h_files = ["h1", "h2"]
    for h_file in h_files:
        if os.path.isfile("./output_" + h_file + ".txt"):
            os.remove("./output_" + h_file + ".txt")
        if os.path.isfile("./detailed_output_" + h_file + ".txt"):
            os.remove("./detailed_output_" + h_file + ".txt")


def main():
    time_limit = get_time_limit()
    delete_existing_files()
    heuristics = [Heuristic.BLOCKING_CARS, Heuristic.BLOCKED_BLOCKING_CARS]
    list_of_boards = parse_list_of_boards()
    list_of_solutions = read_solutions()
    for j, heuristic in enumerate(heuristics):
        heuristic_data = OverallData()
        print("Running with heuristic function " + str(j + 1))
        for i, board in enumerate(list_of_boards):
            print("Solving board number " + str(i + 1))
            data = Data(i, heuristic, time_limit)
            solution = solve_board(board, data)
            data.add_optimality(solution, list_of_solutions[i])
            heuristic_data.add_data(data)
        heuristic_data.print_avgs()
    print("Finished")


main()
