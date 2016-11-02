import math
import sys
from collections import defaultdict


def heuristic_cost_estimate(location, goal):
    return math.sqrt((location.x - goal.x) ** 2 + (location.y - goal.y) ** 2)


def processGrid(goal, occupancy):
    """
    Adapted from https://en.wikipedia.org/wiki/A*_search_algorithm using straight-line distance as the heuristic

    :param start:
    :param goal:
    :param occupancy:
    :return:
    """

    visited = defaultdict(lambda: sys.maxint)
    next_destination = {}
    frontier = {goal: 0}

    while frontier:
        position, cost_so_far = frontier.popitem()
        for dy in xrange(-1, 2):
            for dx in xrange(-1, 2):
                neighbor_position = position[0] + dy, position[1] + dx

                if 0 <= neighbor_position[0] < len(occupancy) and 0 <= neighbor_position[1] < len(occupancy[0]):

                    if occupancy[neighbor_position[0]][neighbor_position[1]] > .9:

                        dist = math.sqrt(dy ** 2 + dx ** 2)
                        if neighbor_position not in visited:
                            frontier[neighbor_position] = cost_so_far + dist
                        if visited[neighbor_position] > cost_so_far + dist:
                            visited[neighbor_position] = cost_so_far + dist
                            next_destination[neighbor_position] = position

    return next_destination


print processGrid((2, 2), [
    [1, 1, 1],
    [1, 0, 0],
    [1, 1, 1]
])
