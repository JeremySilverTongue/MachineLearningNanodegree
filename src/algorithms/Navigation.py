import math
import sys
from Queue import PriorityQueue


def heuristic_cost_estimate(location, goal):
    return math.sqrt((location.x - goal.x) ** 2 + (location.y - goal.y) ** 2)


UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
UP_LEFT = "up_left"
UP_RIGHT = "up_right"
DOWN_LEFT = "down_left"
DOWN_RIGHT = "down_right"

GOAL = "goal"

#
directions = {
    RIGHT: (0, 1),
    UP_RIGHT: (-1, 1),
    UP: (-1, 0),
    UP_LEFT: (-1, -1),
    LEFT: (0, -1),
    DOWN_LEFT: (1, -1),
    DOWN: (1, 0),
    DOWN_RIGHT: (1, 1),
    GOAL: (0, 0)
}


def process_grid(goal, occupancy, danger_grid, danger_weight=1):
    # visited = [(sys.maxint, None) for _ in xrange(occupancy.shape[0]) for _ in xrange(occupancy.shape[1])]
    visited = [[(sys.maxint, None) for _ in xrange(occupancy.shape[1])] for _ in xrange(occupancy.shape[0])]
    visited[goal[0]][goal[1]] = (0, GOAL)
    frontier = PriorityQueue()
    frontier.put((0, goal))

    while not frontier.empty():
        cost_so_far, position = frontier.get()
        for direction, delta in directions.iteritems():
            dy, dx = -delta[0], -delta[1]

            y, x = neighbor_position = position[0] + dy, position[1] + dx

            if 0 <= y < occupancy.shape[0] and 0 <= x < occupancy.shape[1]:

                danger = danger_grid[y][x]

                if occupancy[y][x] == 1:
                    danger = 1000000

                new_cost = cost_so_far + math.sqrt(dx ** 2 + dy ** 2) + danger * danger_weight

                if visited[y][x][1] is None:
                    frontier.put((new_cost, neighbor_position))
                visited[y][x] = min((new_cost, direction), visited[y][x])

    return visited


def get_path(start, plan):
    path = [start]
    y, x = start
    while plan[y][x][1] != GOAL:
        dy, dx = directions[plan[y][x][1]]
        y += dy
        x += dx
        path.append((y, x))
    return path
