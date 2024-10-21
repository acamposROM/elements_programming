# 18_1 was a DFS prob and this is a DFS where we flip all neighbors with the same value
def flip_bits(maze, start):
    max_x = len(maze) - 1
    max_y = len(maze[0]) - 1
    visited = set()
    queue = []
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    queue.append(start)
    x, y = start
    starting_val = maze[x][y]
    visited.add(start)

    while queue:
        curr = queue.pop()
        x, y = curr
        maze[x][y] = starting_val ^ starting_val
        for delta in dirs:
            dx, dy = delta
            pos = x + dx, y + dy
            if pos in visited:
                continue
            pos_x, pos_y = pos
            visited.add(pos)
            if pos_x < 0 or pos_x > max_x or pos_y < 0 or pos_y > max_y:
                continue
            if maze[pos_x][pos_y] != starting_val:
                continue
            queue.append(pos)

    return maze


pass_one = ([[1, 0, 1, 0], [1, 1, 0, 0], [1, 1, 1, 1], [1, 1, 0, 1]], (0, 0))

res = flip_bits(*pass_one)
print(res)
