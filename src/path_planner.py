import utils
import numpy as np
import matplotlib.pyplot as plt

from a_star import AStar
import utils

ax = plt.axes(projection='3d')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

class PathPlanner(AStar):
    def __init__(self):
        self.plt_path = True
        self.plt_search = True

        if self.plt_path:
            for (x, y, z) in utils.BS_POS_LIST:
                ax.plot3D(x, y, z, 'yo')

    def search(self, start, end):
        path = list(self.astar(start, end))

        if path[-1] != end:
            path.append(end)

        if self.plt_path:
            for i in range(len(path)-1):
                xs = [path[i][0], path[i+1][0]]
                ys = [path[i][1], path[i+1][1]]
                zs = [path[i][2], path[i+1][2]]
                #q = utils.nodeNetworkQualCalc((xs[0], ys[0], zs[0]))
                ax.plot3D(xs, ys, zs, 'ro-')#, alpha=q)
                #plt.pause(0.001)

            ax.plot3D(start[0], start[1], start[2], 'bo')
            ax.plot3D(end[0], end[1], end[2], 'ko')

            plt.show()

        return path

    def heuristic_cost_estimate(self, n1, n2):
        return utils.distanceCalc(n1, n2) * (1 - utils.nodeNetworkQualCalc(n1))

    def distance_between(self, n1, n2):
        return utils.nodeNetworkQualCalc(n2) - utils.nodeNetworkQualCalc(n1)

    def neighbors(self, node):
        x, y, z = node

        if self.plt_search:
            ax.plot3D(x, y, z, 'go')
            plt.pause(0.001)

        nlist = [(nx, ny, nz) for nx, ny, nz in[(x, y, z - 3), (x, y, z + 3), (x, y - 3, z), (x, y - 3, z - 3), (x, y - 3, z + 3), (x, y + 3, z), (x, y + 3, z - 3), (x, y + 3, z + 3), (x - 3, y, z), (x - 3, y, z - 3), (x - 3, y, z + 3), (x - 3, y - 3, z), (x - 3, y - 3, z - 3), (x - 3, y - 3, z + 3), (x - 3, y + 3, z), (x - 3, y + 3, z - 3), (x - 3, y + 3, z + 3), (x + 3, y, z), (x + 3, y, z - 3), (x + 3, y, z + 3), (x + 3, y - 3, z), (x + 3, y - 3, z - 3), (x + 3, y - 3, z + 3), (x + 3, y + 3, z), (x + 3, y + 3, z - 3), (x + 3, y + 3, z + 3)]]
        
        return nlist

    def is_goal_reached(self, current, goal):
        return current == goal or utils.distanceCalc(current, goal) < 4