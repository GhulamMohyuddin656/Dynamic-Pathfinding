# search.py

import time
import math
import heapq

# ---------------- HEURISTICS ---------------- #

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def chebyshev(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

HEURISTICS = {
    "Manhattan": manhattan,
    "Euclidean": euclidean,
    "Chebyshev": chebyshev
}

DIRS = [(1,0),(-1,0),(0,1),(0,-1)]

# ---------------- A* ---------------- #

def a_star(start, goal, grid, heuristic):
    start_time = time.perf_counter()
    rows = len(grid)
    cols = len(grid[0])

    open_heap = []
    heapq.heappush(open_heap, (0, start))

    came_from = {}
    g_score = {start: 0}
    nodes_expanded = 0
    closed = set()

    while open_heap:
        _, current = heapq.heappop(open_heap)

        if current == goal:
            path = reconstruct(came_from, current)
            exec_time = (time.perf_counter() - start_time) * 1000
            return path, nodes_expanded, exec_time

        if current in closed:
            continue

        closed.add(current)
        nodes_expanded += 1

        for dr, dc in DIRS:
            nr, nc = current[0] + dr, current[1] + dc

            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == 1:
                    continue

                tentative_g = g_score[current] + 1

                if tentative_g < g_score.get((nr, nc), float('inf')):
                    came_from[(nr, nc)] = current
                    g_score[(nr, nc)] = tentative_g
                    f = tentative_g + heuristic((nr, nc), goal)
                    heapq.heappush(open_heap, (f, (nr, nc)))

    exec_time = (time.perf_counter() - start_time) * 1000
    return None, nodes_expanded, exec_time


# ---------------- RBFS ---------------- #

def rbfs(start, goal, grid, heuristic):
    start_time = time.perf_counter()
    rows = len(grid)
    cols = len(grid[0])
    nodes_expanded = 0

    class Node:
        def __init__(self, pos, g, parent):
            self.pos = pos
            self.g = g
            self.h = heuristic(pos, goal)
            self.f = self.g + self.h
            self.parent = parent

    def reconstruct_path(node):
        path = []
        while node:
            path.append(node.pos)
            node = node.parent
        return list(reversed(path))

    def rbfs_recursive(node, f_limit):
        nonlocal nodes_expanded

        if node.pos == goal:
            return node, node.f

        nodes_expanded += 1

        successors = []
        for dr, dc in DIRS:
            nr, nc = node.pos[0] + dr, node.pos[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == 0:
                    child = Node((nr, nc), node.g + 1, node)
                    successors.append(child)

        if not successors:
            return None, float('inf')

        successors.sort(key=lambda x: x.f)

        while True:
            best = successors[0]
            if best.f > f_limit:
                return None, best.f

            alternative = successors[1].f if len(successors) > 1 else float('inf')

            result, best.f = rbfs_recursive(best, min(f_limit, alternative))

            if result is not None:
                return result, best.f

            successors.sort(key=lambda x: x.f)

    start_node = Node(start, 0, None)
    result, _ = rbfs_recursive(start_node, float('inf'))

    exec_time = (time.perf_counter() - start_time) * 1000

    if result:
        return reconstruct_path(result), nodes_expanded, exec_time

    return None, nodes_expanded, exec_time


def reconstruct(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path