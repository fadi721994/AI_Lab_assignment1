from utils import *
import time


def main():
    opt = 0
    too_opt = 0
    not_opt = 0
    no_sol = 0
    list_of_boards = parse_list_of_boards()
    list_of_solutions = read_solutions()
    times = []
    for i, board in enumerate(list_of_boards):
        start = time.time()
        solution = solve_board(board)
        end = time.time()
        diff = end - start
        times.append(diff)
        print("Solution " + str(i + 1) + " is")
        if solution is None:
            print("No solution was found")
            no_sol = no_sol + 1
        else:
            val = validate_solution(list_of_solutions[i], solution)
            if val == 1:
                too_opt = too_opt + 1
                print("Too optimal")
            elif val == 0:
                opt = opt + 1
                print("Optimal")
            elif val == -1:
                not_opt = not_opt + 1
                print("Not optimal")
            print(solution)
        print("Time took is " + str(round(diff, 3)) + " seconds")
    print("Too optimal: " + str(too_opt))
    print("Optimal: " + str(opt))
    print("Not optimal: " + str(not_opt))
    print("No solution: " + str(no_sol))
    for i, t in enumerate(times):
        print("Time took to solve " + str(i + 1) + " is " + str(round(t, 3)) + " seconds")

    avg = sum(times)/len(times)
    print("Average time is " + str(avg) + " seconds")
    print("Overall time is " + str(sum(times)))
main()
