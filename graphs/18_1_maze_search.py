# 10-09-2024 TIME: 1:02:58s


def search_maze(maze, start, end):
    print(f"Starting at {start} ending at {end}")
    max_x = len(maze) - 1
    max_y = len(maze[0]) - 1
    visited = set()
    queue = []
    dirs = [(1, 1), (1, 0), (0, 1), (-1, -1), (-1, 0), (0, -1)]
    x, y = start
    if maze[x][y] == 0:
        return []

    queue.append(start)

    def recurse(queue):
        curr = queue[-1]
        visited.add(curr)
        x, y = curr
        ans = []
        for mov in dirs:
            dx, dy = mov
            pos = (x + dx, y + dy)
            pos_x, pos_y = pos
            if pos in visited:
                continue

            visited.add(pos)
            if pos_x < 0 or pos_x > max_x or pos_y < 0 or pos_y > max_y:
                continue

            if maze[pos_x][pos_y] == 1:
                queue.append(pos)
                if pos == end:
                    return pos
                ans = recurse(queue)
                if ans:
                    return queue

        queue.pop()
        return ans

    return recurse(queue)


pass_two = ([[1, 1, 0, 0], [0, 0, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1]], (0, 0), (3, 3))

pass_one = ([[1, 0, 1, 0], [1, 1, 0, 0], [1, 1, 1, 1], [1, 1, 0, 1]], (0, 0), (3, 3))

fail_one = ([[1, 0, 1, 0], [1, 1, 0, 0], [1, 0, 0, 1], [1, 1, 0, 1]], (0, 0), (3, 3))

result = search_maze(*pass_one)
print(result)

result = search_maze(*pass_two)
print(result)

result = search_maze(*fail_one)
print(result)
