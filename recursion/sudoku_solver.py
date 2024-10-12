def pp_sudoku(puzzle):
    em_dash = '—'
    line_indices = [2, 5]
    for i, row in enumerate(puzzle):
        for j, c in enumerate(row):
            print(c, end=' ')
            if j in line_indices:
                print('|', end = ' ')
        print('')
        if i in line_indices:
            print(em_dash * 21)


def pp_2d(matrix):
    for r in matrix:
        print(r)

def sudoku_solver(puzzle):
    pp_sudoku(puzzle)
    # storing row, col and grid states for faster checking
    # of already used up numbers in each of those positions
    rows_set = {k: set() for k in range(9)}
    cols_set = {k: set() for k in range(9)}

    # grids index corresponds to each 3x3 section starting from the upper left corner
    # 0 1 2
    # 3 4 5
    # 6 7 8
    grid_set = {k: set() for k in range(9)} 
    invalid_vals = {(i, j): set() for i in range(9) for j in range(9)}
    
    first_zero_found = False
    start = ()
    # iterate through puzzle to start filling in hashes
    for r in puzzle:
        for c in r:
            val = puzzle[r][c]
            if not first_zero_found and val == 0:
                start = (r, c)
            rows_set[r].add(val)
            cols_set[c].add(val)
            # How do we figure out the grid?
            # 0,0 to 2,2 grid 0
            # 0,3 to 2,5 grid 1
            # 0,6 to 2,8 grid 2
            # 3,0 to 5,2 grid 3
            # 3,3 to 5,5 grid 4
            # 3,6 to 5,8 grid 5
            # 6,0 to 8,2 grid 6
            # 6,3 to 8,5 grid 7
            # 6,6 to 8,8 grid 8
    return 0

puzzle_one = [
    [0, 1, 2, 0, 0, 0, 6, 0, 8],
    [0, 0, 0, 0, 7, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 9, 3, 0, 5],
    [1, 2, 3, 0, 0, 6, 0, 0, 0],
    [4, 0, 0, 8, 0, 0, 0, 1, 3],
    [0, 8, 0, 0, 1, 0, 0, 5, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 8, 4, 7, 0, 2],
    [0, 0, 0, 7, 3, 2, 5, 0, 1]
]

solution_one = [
    [9, 1, 2, 3, 4, 5, 6, 7, 8],
    [3, 4, 5, 6, 7, 8, 1, 2, 9],
    [6, 7, 8, 1, 2, 9, 3, 4, 5],
    [1, 2, 3, 4, 5, 6, 8, 9, 7],
    [4, 5, 6, 8, 9, 7, 2, 1, 3],
    [7, 8, 9, 2, 1, 3, 4, 5, 6],
    [2, 3, 7, 5, 6, 1, 9, 8, 4],
    [5, 6, 1, 9, 8, 4, 7, 3, 2],
    [8, 9, 4, 7, 3, 2, 5, 6, 1]
]

sudoku_solver(puzzle_one)
