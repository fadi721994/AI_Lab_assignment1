import math
import time
from heuristic import Heuristic
from utils import validate_solution


class Data:
    def __init__(self, board_num, heuristic, time_limit):
        self.board_num = board_num
        self.heuristic = heuristic
        self.solution = ''
        self.scanned_nodes = 0
        self.solution_depth = 0
        self.max_depth = 0
        self.min_depth = math.inf
        self.depths = []
        self.avg_depth = 0
        self.start_time = time.time()
        self.end_time = 0
        self.run_time = 0
        self.heuristic_values = []
        self.heuristic_avg = 0
        self.time_limit = time_limit
        self.optimal = 0

    # Given the open list, find the tree depths data, minimum, maximum and average.
    def find_tree_depth_data(self, open_list):
        for entry in open_list.queue:
            state = entry.state
            self.depths.append(state.depth)
        self.min_depth = min(self.depths)
        self.max_depth = max(self.depths)
        self.avg_depth = sum(self.depths)/len(self.depths)

    def get_penetrance(self):
        return self.solution_depth / self.scanned_nodes

    def get_ebf(self):
        return self.scanned_nodes ** (1 / self.solution_depth)

    # Finalize the data and write to the output files.
    def finalize(self, solution, sol_depth, open_list):
        self.end_time = time.time()
        self.run_time = self.end_time - self.start_time
        self.solution = solution
        self.solution_depth = sol_depth
        self.heuristic_avg = sum(self.heuristic_values) / len(self.heuristic_values)
        penetrance = self.get_penetrance()
        ebf = self.get_ebf()
        self.find_tree_depth_data(open_list)
        if self.run_time > self.time_limit:
            self.solution = "FAILED"

        if self.heuristic == Heuristic.BLOCKING_CARS:
            h_file = 'h1'
        else:
            h_file = 'h2'

        with open("output_" + h_file + ".txt", 'a') as file:
            file.write(self.solution + "\n")
        with open("detailed_output_" + h_file + ".txt", 'a') as file:
            file.write("Board number " + str(self.board_num + 1) + "\n")
            file.write("---------------------------------------------------------------\n")
            file.write("Solution: " + self.solution + "\n")
            file.write("Solution depth: " + str(self.solution_depth) + "\n")
            file.write("Scanned nodes: " + str(self.scanned_nodes) + "\n")
            file.write("Penetrance: " + str(penetrance) + "\n")
            file.write("Run time: " + str(self.run_time) + "\n")
            file.write("Heuristic function average: " + str(self.heuristic_avg) + "\n")
            file.write("EBF: " + str(ebf) + "\n")
            file.write("Minimum tree depth: " + str(self.min_depth + 1) + "\n")
            file.write("Average tree depth: " + str(self.avg_depth + 1) + "\n")
            file.write("Maximum tree depth: " + str(self.max_depth + 1) + "\n")

    # Append to the data detailed output file whether the solution is optimal or not.
    def add_optimality(self, solution, suggested_solution):
        opt_str = ''
        if solution is None:
            opt_str = 'Failed to find solution'
        else:
            self.optimal = validate_solution(suggested_solution, solution)
            if self.optimal == 1:
                opt_str = 'Solution has less steps than the suggested solution'
            elif self.optimal == 0:
                opt_str = 'Solution has the same amount of steps as the suggested solution'
            elif self.optimal == -1:
                opt_str = 'Solution has more steps than the suggested solution'
        if self.heuristic == Heuristic.BLOCKING_CARS:
            h_file = 'h1'
        else:
            h_file = 'h2'
        with open("detailed_output_" + h_file + ".txt", 'a') as file:
            file.write(opt_str + "\n")
            file.write("---------------------------------------------------------------\n\n\n")
