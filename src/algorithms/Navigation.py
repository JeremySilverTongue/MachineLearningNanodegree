import math
import sys
from Queue import PriorityQueue
import numpy as np

def heuristic_cost_estimate(location, goal):
    return math.sqrt((location.x - goal.x) ** 2 + (location.y - goal.y) ** 2)


UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
GOAL = "goal"


def process_grid(goal, occupancy, danger_grid, danger_weight=1):
    # visited = [(sys.maxint, None) for _ in xrange(occupancy.shape[0]) for _ in xrange(occupancy.shape[1])]
    visited = [[(sys.maxint, None) for _ in xrange(occupancy.shape[1])] for _ in xrange(occupancy.shape[0])]
    visited[goal[0]][goal[1]] = (0, GOAL)
    frontier = PriorityQueue()
    frontier.put((0, goal))

    while not frontier.empty():
        print frontier
        cost_so_far, position = frontier.get()
        for dy, dx, direction in [(-1, 0, DOWN), (1, 0, UP), (0, 1, LEFT), (0, -1, RIGHT)]:

            y, x = neighbor_position = position[0] + dy, position[1] + dx

            if 0 <= y < occupancy.shape[0] and 0 <= x < occupancy.shape[1]:

                danger = danger_grid[y][x]

                if occupancy[y][x] == 1:
                    danger = 1000000

                new_cost = cost_so_far + 1 + danger * danger_weight

                if visited[y][x][1] is None:
                    frontier.put((new_cost, neighbor_position))
                visited[y][x] = min((new_cost, direction), visited[y][x])

    return visited


out = process_grid((2, 2), np.array([
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
]),
                   np.array([
                       [.0, .0, .1],
                       [.0, 10000, .9],
                       [.0, .0, .1]
                   ]), danger_weight=1

                   )

for row in out:
    print row
