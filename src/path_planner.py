import utils
import numpy as np
import matplotlib.pyplot as plt

from a_star import AStar
import utils

class PathPlanner(AStar):
    def __init__(self, plt_path=False, plt_search=False):
        self.plt_path = plt_path
        self.plt_search = plt_search

    def search(self, start, end):
        path = list(self.astar(start, end))
        if path[-1] != end:
            path.append(end)
        if self.plt_path:
            for i in range(len(path)-1):
                xs = [path[i][0], path[i+1][0]]
                ys = [path[i][1], path[i+1][1]]
                zs = [path[i][2], path[i+1][2]]
                ax.plot3D(xs, ys, zs, 'ro-')
                #plt.pause(0.001)
            ax.plot3D(start[0],start[1], start[2], 'bo')
            ax.plot3D(end[0],end[1], end[2], 'ko')
            plt.show()
        return path

    def heuristic_cost_estimate(self, n1, n2):
        # Calc net quality for n1
        mult = 0
        for (x, y, z) in bs_list:
            dist2bs = utils.distanceCalc(n1, (x, y, z))
            if dist2bs <= 11:
                mult += 0.3666667*dist2bs - 0.04642857*dist2bs**2 + 0.001190476*dist2bs**3

        dist2end = utils.distanceCalc(n1, n2) * (1 - mult)
        return dist2end

    def distance_between(self, n1, n2):
        n1Qual = 0
        n2Qual = 0
        for (x, y, z) in bs_list:
            n1dist2bs = utils.distanceCalc(n1, (x, y, z))
            if n1dist2bs <= 11:
                n1Qual += 0.3666667*n1dist2bs - 0.04642857*n1dist2bs**2 + 0.001190476*n1dist2bs**3
            n2dist2bs = utils.distanceCalc(n2, (x, y, z))
            if n2dist2bs <= 11:
                n2Qual += 0.3666667*n2dist2bs - 0.04642857*n2dist2bs**2 + 0.001190476*n2dist2bs**3
        return n2Qual - n1Qual

    def neighbors(self, node):
        x, y, z = node
        if self.plt_search:
            ax.plot3D(x, y, z, 'go')
            plt.pause(0.001)
        nlist = [(nx, ny, nz) for nx, ny, nz in[(x, y, z - 3), (x, y, z + 3), (x, y - 3, z), (x, y - 3, z - 3), (x, y - 3, z + 3), (x, y + 3, z), (x, y + 3, z - 3), (x, y + 3, z + 3), (x - 3, y, z), (x - 3, y, z - 3), (x - 3, y, z + 3), (x - 3, y - 3, z), (x - 3, y - 3, z - 3), (x - 3, y - 3, z + 3), (x - 3, y + 3, z), (x - 3, y + 3, z - 3), (x - 3, y + 3, z + 3), (x + 3, y, z), (x + 3, y, z - 3), (x + 3, y, z + 3), (x + 3, y - 3, z), (x + 3, y - 3, z - 3), (x + 3, y - 3, z + 3), (x + 3, y + 3, z), (x + 3, y + 3, z - 3), (x + 3, y + 3, z + 3)]]
        return nlist

    def is_goal_reached(self, current, goal):
        return current == goal or utils.distanceCalc(current, goal) < 4


ax = plt.axes(projection='3d')
bs_list = [(25, 25, 23), (25, 80, 23), (80, 25, 23), (80, 80, 23)]
for (x, y, z) in bs_list:
    ax.plot3D(x, y, z, 'yo')
PathPlanner(True, False).search(utils.START_POS, utils.END_POS)