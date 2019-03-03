from utils import *


def main():
    opt = 0
    too_opt = 0
    not_opt = 0
    no_sol = 0
    list_of_boards = parse_list_of_boards()
    list_of_solutions = read_solutions()
    for i, board in enumerate(list_of_boards):
        solution = solve_board(board)
        print("Solution " + str(i + 1) + " is")
        if solution is None:
            print("No solution was found")
            no_sol = no_sol + 1
        else:
            val = validate_solution(list_of_solutions[i], solution)
            if val == 1:
                too_opt = too_opt + 1
            elif val == 0:
                opt = opt + 1
            elif val == -1:
                not_opt = not_opt + 1
            print(solution)
    print("Too optimal: " + str(too_opt))
    print("Optimal: " + str(opt))
    print("Not optimal: " + str(not_opt))
    print("No solution: " + str(no_sol))


main()
