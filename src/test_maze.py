
from a_star import AStar
import sys
import math
import matplotlib.pyplot as plt
import utils
import numpy as np

ax = plt.axes(projection='3d')

class MazeSolver(AStar):

    def __init__(self):
        pass

    def heuristic_cost_estimate(self, n1, n2):
        return utils.distanceCalc(n1, n2)

    def distance_between(self, n1, n2):
        return 3

    def neighbors(self, node):
        x, y, z = node
        return[(nx, ny, nz) for nx, ny, nz in[(x, y, z - 3),
                                                (x, y, z + 3),
                                                (x, y - 3, z),
                                                (x, y - 3, z - 3),
                                                (x, y - 3, z + 3),
                                                (x, y + 3, z),
                                                (x, y + 3, z - 3),
                                                (x, y + 3, z + 3),
                                                (x - 3, y, z),
                                                (x - 3, y, z - 3),
                                                (x - 3, y, z + 3),
                                                (x - 3, y - 3, z),
                                                (x - 3, y - 3, z - 3),
                                                (x - 3, y - 3, z + 3),
                                                (x - 3, y + 3, z),
                                                (x - 3, y + 3, z - 3),
                                                (x - 3, y + 3, z + 3),
                                                (x + 3, y, z),
                                                (x + 3, y, z - 3),
                                                (x + 3, y, z + 3),
                                                (x + 3, y - 3, z),
                                                (x + 3, y - 3, z - 3),
                                                (x + 3, y - 3, z + 3),
                                                (x + 3, y + 3, z),
                                                (x + 3, y + 3, z - 3),
                                                (x + 3, y + 3, z + 3)]]

    def is_goal_reached(self, current, goal):
        return current == goal or utils.distanceCalc(current, goal) < 3


def testMaze():
    start = (1, 1, 1)
    goal = (120, 80, 150)

    path = list(MazeSolver().astar(start, goal))

    if path[-1] != goal:
        path.append(goal)

    for (x, y, z) in path:
        ax.plot3D(x, y, z, 'ro')

    ax.set_xticks(np.arange(0, 150, 20))
    ax.set_yticks(np.arange(0, 150, 20))
    ax.set_zticks(np.arange(0, 150, 20))

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    plt.show()

testMaze()