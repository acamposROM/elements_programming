def pp_sudoku(puzzle):
    em_dash = "—"
    line_indices = [2, 5]
    for i, row in enumerate(puzzle):
        for j, c in enumerate(row):
            print(c, end=" ")
            if j in line_indices:
                print("|", end=" ")
        print("")
        if i in line_indices:
            print(em_dash * 21)
    print()


def pp_2d(matrix):
    for r in matrix:
        print(r)


def sudoku_verify(puzzle):
    rows_set = {k: set() for k in range(9)}
    cols_set = {k: set() for k in range(9)}
    grid_set = {k: set() for k in range(9)}
    grid_zone = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    grid_index = [0, 0, 0, 1, 1, 1, 2, 2, 2]
    for r, row in enumerate(puzzle):
        for c, val in enumerate(row):
            if val < 1 or val > 9:
                return False
            grid_x, grid_y = grid_index[r], grid_index[c]
            grid_loc = grid_zone[grid_x][grid_y]
            if val in rows_set[r] or val in cols_set[c] or val in grid_set[grid_loc]:
                return False
            rows_set[r].add(val)
            cols_set[c].add(val)
            grid_set[grid_loc].add(val)
    return True


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
    # In sudoku you also have to validate there are 1-9s in each 3x3 square
    # of the puzzle. I created an array that helps the program figure out given
    # r,c position what grid it falls in. We just need a 3x3 array to hold the
    # grid values. We use grid_index to map the sudoku r,c to the grid zone indices
    # this takes 2*O(9) space and O(3) look ups (find x y, then find the grid val)
    grid_zone = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    grid_index = [0, 0, 0, 1, 1, 1, 2, 2, 2]

    # invalid_vals = {(i, j): set() for i in range(9) for j in range(9)}
    fill_list = []
    # iterate through puzzle to start filling in hashes
    for r, row in enumerate(puzzle):
        for c, val in enumerate(row):
            if val == 0:
                fill_list.append((r, c))
                continue
            rows_set[r].add(val)
            cols_set[c].add(val)
            grid_x, grid_y = grid_index[r], grid_index[c]
            grid_loc = grid_zone[grid_x][grid_y]
            grid_set[grid_loc].add(val)

    if debug:
        print(rows_set)
        print(cols_set)
        print(grid_set)

    def recurse(fill_list):
        curr = fill_list.pop()
        x, y = curr
        grid_x, grid_y = grid_index[x], grid_index[y]
        grid_loc = grid_zone[grid_x][grid_y]
        for val in range(1, 10):
            if val in rows_set[x] or val in cols_set[y] or val in grid_set[grid_loc]:
                continue
            rows_set[x].add(val)
            cols_set[y].add(val)
            grid_set[grid_loc].add(val)
            if fill_list and recurse(fill_list) == 0:
                rows_set[x].remove(val)
                cols_set[y].remove(val)
                grid_set[grid_loc].remove(val)
            else:
                puzzle[x][y] = val
                return val
        fill_list.append(curr)
        return 0

    recurse(fill_list)
    return puzzle


debug = False
puzzle_one = [
    [0, 1, 2, 0, 0, 0, 6, 0, 8],
    [0, 0, 0, 0, 7, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 9, 3, 0, 5],
    [1, 2, 3, 0, 0, 6, 0, 0, 0],
    [4, 0, 0, 8, 0, 0, 0, 1, 3],
    [0, 8, 0, 0, 1, 0, 0, 5, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 8, 4, 7, 0, 2],
    [0, 0, 0, 7, 3, 2, 5, 0, 1],
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
    [8, 9, 4, 7, 3, 2, 5, 6, 1],
]

print(sudoku_verify(solution_one))
result = sudoku_solver(puzzle_one)
pp_sudoku(result)
print(f"Valid Sudoku Answer: {sudoku_verify(result)}")
