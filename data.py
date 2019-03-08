import math
import time


class Data:
    def __init__(self, board_num, heuristic):
        self.board_num = board_num
        self.heuristic = heuristic
        self.solution = []
        self.scanned_nodes = 0
        self.solution_depth = 0
        self.max_depth = 0
        self.min_depth = math.inf
        self.avg_depth = 0
        self.depths = []
        self.start_time = time.time()
        self.end_time = 0
        self.run_time = 0
        self.heuristic_values = []
        self.heuristic_avg = 0

    def get_penetrance(self):
        return self.solution_depth / self.scanned_nodes

    def get_ebf(self):
        return self.scanned_nodes ** (1 / self.solution_depth)

    def finalize(self):
        self.end_time = time.time()
        self.run_time = self.end_time - self.start_time
        print("Grid " + str(self.board_num + 1))
        print("Time to solve is: " + str(round(self.run_time, 3)))

