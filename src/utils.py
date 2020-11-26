import numpy as np
import matplotlib.pyplot as plt
import vg
import itertools

# [X, Y, Z]
# X = Longitude, Y = Latitude, Z = Altitude
# Sizes in meters

# Area consts
AREA_SIZE = [400, 400, 120]
AREA_GROUND_HEIGHT = 1

# Base Station consts
BS_SIZE = [3, 3, 25]
BS_RANGE = 40
BS_ANT_HEIGHT = 23
BS_POS_LIST = []

def cart2sph(coord):
    x, y, z = coord
    hxy = np.hypot(x, y)
    r = np.hypot(hxy, z)
    el = np.arctan2(hxy, z) # z-axis down, switch for xy-plane up
    az = np.arctan2(y, x)
    return r, np.rad2deg(az), np.rad2deg(el)    # radius, theta, phi

def distanceCalc(A, B):
    a = np.array((A[0], A[1], A[2]))
    b = np.array((B[0], B[1], B[2]))
    x, y, z = b - a
    hxy = np.hypot(x, y)
    r = np.hypot(hxy, z)
    return r

def angleCalc(A, B):
    a = np.array((A[0], A[1], A[2]))
    b = np.array((B[0], B[1], B[2]))
    if np.array_equal(a, b):
        return 0
    c = b - a   # calc difference vector
    z = np.array(([0, 0, 1])) # unit vector
    return vg.angle(c, z)

def nodeNetworkQualCalc(node):
    # Store quality for each valid bs
    qualList = []
    for (x, y, _) in BS_POS_LIST:
        a = np.array([node[0], node[1], node[2]])
        b = np.array([x+1, y+1, BS_ANT_HEIGHT]) # add 1 since it is 3x3

        dist, _, ang = cart2sph(b-a)

        if dist <= BS_RANGE+1:
            qdist = 0.03174603 + 0.139914*dist - 0.005735367*dist**2 + 0.00005606192*dist**3
            qdist = max(0, min(1, qdist))

            qang = -2.5 + 0.0722222*ang - 0.00037037*ang**2
            qang = max(0, min(1, qang))

            q = (0.7 * qang) + (0.3 * qdist) # TODO: ADD SIMULATED QUALITY FOR THIS BS
            qualList.append(q)

    # Evenly weighted sum for each quality => [0, 1]
    totalQual = 0
    if len(qualList) > 0:
        weight = 1/len(qualList)    
        for qual in qualList:
            totalQual += weight * qual

    return totalQual

def threshSmoothPath(initialPath, thresh):
    seq = itertools.product([0,1], repeat=6)

    bestQual = 0
    bestPath = []

    threshQual = 1
    threshPath = []

    for i in list(seq):  
        newPath = smoothPath(initialPath, i)

        avgQual = calcPathAvgQual(newPath)

        if avgQual > bestQual:
            bestQual = avgQual
            bestPath = newPath

        if avgQual < threshQual and avgQual >= thresh:
            threshQual = avgQual
            threshPath = newPath
            
    return threshQual, threshPath, bestQual, bestPath

# 0 = insert midpoints, 1 = avg midpoints
def smoothPath(initialPath, seq):
    points = initialPath
    for i in seq:
        if i == 0:
            points = insertMidpoints(points)
        elif i == 1:
            points = avgMidpoints(points)
    return points

def insertMidpoints(points):
    path = []
    for i in range(len(points)-1):
        x3 = 0.5 * points[i][0] + 0.5 * points[i+1][0]
        y3 = 0.5 * points[i][1] + 0.5 * points[i+1][1]
        z3 = 0.5 * points[i][2] + 0.5 * points[i+1][2]
        path.append((points[i][0], points[i][1], points[i][2]))
        path.append((x3, y3, z3))
    path.append(points[-1])
    return path

def avgMidpoints(points):
    path = [points[0]]
    for i in range(len(points)-1):
        x3 = 0.5 * points[i][0] + 0.5 * points[i+1][0]
        y3 = 0.5 * points[i][1] + 0.5 * points[i+1][1]
        z3 = 0.5 * points[i][2] + 0.5 * points[i+1][2]
        path.append((x3, y3, z3))
    path.append(points[-1])
    return path

def getCornerPoints(path):
    cornerPoints = [path[0]]
    for i in range(1, len(path)-1):
        x1 = path[i-1][0]
        y1 = path[i-1][1]
        z1 = path[i-1][2]

        x2 = path[i][0]
        y2 = path[i][1]
        z2 = path[i][2]

        x3 = path[i+1][0]
        y3 = path[i+1][1]
        z3 = path[i+1][2]

        v1 = [(x2 - x1), (y2 - y1), (z2 - z1)]
        v2 = [(x3 - x1), (y3 - y1), (z3 - z1)]

        if not vg.almost_collinear(v1, v2):
            cornerPoints.append((x2, y2, z2))

    cornerPoints.append(path[-1])
    return cornerPoints

def calcPathAvgQual(path):
    qual = 0
    for node in path:
        qual += nodeNetworkQualCalc(node)
    return qual/len(path)

def calcPathDist(path):
    dist = 0
    for i in range(len(path)-1):
        dist += distanceCalc(path[i], path[i+1])
    dist += distanceCalc(path[-2], path[-1])
    return dist

def plotPath(paths):
    if len(paths) > 3:
        return

    ax = plt.axes(projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    # Plot the base station antennas
    for (x, y, _) in BS_POS_LIST:
        ax.plot3D(x+1, y+1, BS_ANT_HEIGHT, 'yo')
    
    color = ['ro-', 'go-', 'yo-']
    ci = 0

    # Plot the paths
    for path in paths:
        for i in range(len(path)-1):
            xs = [path[i][0], path[i+1][0]]
            ys = [path[i][1], path[i+1][1]]
            zs = [path[i][2], path[i+1][2]]
            ax.plot3D(xs, ys, zs, color[ci])
        ci += 1
    ax.plot3D(path[0][0], path[0][1], path[0][2], 'bo-')
    ax.plot3D(path[-1][0], path[-1][1], path[-1][2], 'ko-')

    plt.show()

def vizQualityPattern():
    ax = plt.axes(projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    for y in range(-41, 122):
        for z in range(-17, 64):
            if y == 0 and z == 23:
                continue
            q = nodeNetworkQualCalc((0, y, z))
            if q > 0.9:
                ax.plot(0, y, z, marker='o', color='#C73E1D', alpha=1)
            elif q > 0.8:
                ax.plot(0, y, z, marker='o', color='#F18F01', alpha=1)
            elif q > 0.7:
                ax.plot(0, y, z, marker='o', color='#D5B942', alpha=1)
            elif q > 0.6:
                ax.plot(0, y, z, marker='o', color='#330F0A', alpha=1)
            elif q > 0.5:
                ax.plot(0, y, z, marker='o', color='#EDAFB8', alpha=1)
            elif q > 0.4:
                ax.plot(0, y, z, marker='o', color='#B1CC74', alpha=1)
            elif q > 0.3:
                ax.plot(0, y, z, marker='o', color='#E8FCC2', alpha=1)
            elif q > 0.2:
                ax.plot(0, y, z, marker='o', color='#D0F4EA', alpha=1)
            elif q > 0.1:
                ax.plot(0, y, z, marker='o', color='#829399', alpha=1)
            elif q > 0:
                ax.plot(0, y, z, marker='o', color='#545F66', alpha=1)

    ax.view_init(elev=0, azim=0)
    plt.show()

# Create BS in hex grid
# for i in range(1, BS_NUM+1):
#     for j in range(1, BS_NUM):
#         loc = (BS_DIST_BETWEEN * i, BS_DIST_BETWEEN * j, BS_ANT_HEIGHT)
#         # if i % 2 == 0:
#         #     loc = (BS_DIST_BETWEEN * i, BS_DIST_BETWEEN * j, BS_ANT_HEIGHT)
#         # else:
#         #     loc = (BS_DIST_BETWEEN * i, (BS_DIST_BETWEEN * j) + BS_DIST_BETWEEN/2, BS_ANT_HEIGHT)
#         BS_POS_LIST.append(loc)

# Distribution of quality and angle weight at 0-deg y0 = 0.3, y1 = 0.5 y2 = 0.7
# x = np.arange(0, 7, 1)
# y0 = (0.93,0.78,0.44,0.30,0.44,0.78,0.93)
# y1 = (0.95,0.84,0.60,0.50,0.60,0.84,0.95)
# y2 = (0.97,0.91,0.76,0.70,0.76,0.91,0.97)
# plt.plot(x, y0, 'ro-')
# plt.plot(x, y1, 'bo-')
# plt.plot(x, y2, 'yo-')
# plt.show()

# Create gif
# ax = plt.axes(projection='3d')
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')

# n = PathPlanner().neighbors((0, 0, 0))
# for (x, y, z) in n:
#     ax.plot([0, x], [0, y], [0, z], 'ro-')

# ax.plot(0, 0, 0, 'bo')

# for ii in range(0,90,5):
#     ax.view_init(elev=20., azim=ii)
#     plt.savefig(".\\movie\\movie%d.png" % ii)

# plt.show()