Dynamic Pathfinding Agent

A grid-based AI pathfinding system implementing A* and Recursive Best-First Search (RBFS) with support for dynamic obstacle replanning.

Features

A* Search

RBFS (memory-efficient search)

Manhattan, Euclidean, and Chebyshev heuristics

Interactive grid (mouse-based wall placement)

Random maze generation

Dynamic obstacle spawning

Real-time replanning

Performance metrics (nodes expanded, time, path cost)

Algorithms
A*

Uses:

𝑓
(
𝑛
)
=
𝑔
(
𝑛
)
+
ℎ
(
𝑛
)
f(n)=g(n)+h(n)

Optimal and complete

Faster in grid environments

Higher memory usage

RBFS

Uses recursive best-first strategy with f-limit.

Memory efficient

Slower than A*

May re-expand nodes

How to Run

Install Python 3.8+

Install dependencies:

pip install pygame

Run:

python main.py
Controls

Left Click → Add wall

Right Click → Remove wall

Generate Maze → Random grid

Toggle Dynamic Mode → Enable obstacle spawning

Select Algorithm → A* or RBFS

Select Heuristic → Manhattan / Euclidean / Chebyshev

Start → Run search

Dynamic Mode

Obstacles spawn during agent movement.

If path becomes blocked, automatic replanning is triggered.

Simulates real-world navigation.

Performance Metrics

Nodes Expanded

Path Cost

Execution Time (ms)

Conclusion

A* performs better in most grid scenarios.

RBFS is memory-efficient but slower.

Heuristic choice significantly impacts performance.
