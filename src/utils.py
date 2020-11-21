import numpy as np
import matplotlib.pyplot as plt
import vg

# [X, Y, Z]
# X = Longitude, Y = Latitude, Z = Altitude
# Sizes in meters

# Area consts
AREA_SIZE = [400, 400, 120]
AREA_GROUND_HEIGHT = 1

# Base Station consts
BS_SIZE = [3, 3, 25]
BS_NUM = 4
BS_RANGE = 10
BS_DIST_BETWEEN = 20
BS_ANT_HEIGHT = 23
BS_POS_LIST = [(10, 11, 10), (10, 31, 10)]

# for i in range(1, BS_NUM+1):
#     for j in range(1, BS_NUM):
#         loc = (BS_DIST_BETWEEN * i, BS_DIST_BETWEEN * j, BS_ANT_HEIGHT)
#         # if i % 2 == 0:
#         #     loc = (BS_DIST_BETWEEN * i, BS_DIST_BETWEEN * j, BS_ANT_HEIGHT)
#         # else:
#         #     loc = (BS_DIST_BETWEEN * i, (BS_DIST_BETWEEN * j) + BS_DIST_BETWEEN/2, BS_ANT_HEIGHT)
#         BS_POS_LIST.append(loc)

# Path consts
START_POS = (1, 1, 1)
END_POS = (15, 35, 13)

# Old consts
MIN_LAT = 51.241700
MAX_LAT = 51.245600
MIN_LON = -114.885100
MAX_LON = -114.879500
LAT_DIFF = 0.000008986175
LON_DIFF = 0.00001432225

def distanceCalc(A, B):
    a = np.array((A[0], A[1], A[2]))
    b = np.array((B[0], B[1], B[2]))
    return np.linalg.norm(a-b)

def angleCalc(A, B):
    a = np.array((A[0], A[1], A[2]))
    b = np.array((B[0], B[1], B[2]))
    if np.array_equal(a, b):
        return 0
    c = b - a   # calc difference vector
    z = np.array(([0, 0, 1])) # unit vector
    return vg.angle(c, z)
    
    # Used to visualize
    # data = [A, B]
    # x, y, z = zip(*data)
    # ax = plt.axes(projection='3d')
    # ax.plot3D(x, y, z, 'ro-')
    # ax.text(B[0], B[1], B[2], "{:.2f}".format(angle))
    # plt.pause(0.05)


# def nodeNetworkQualCalc2(node):
#     qual = 0
#     for (x, y, z) in BS_POS_LIST:
#         dist = distanceCalc(node, (x, y, z))
#         if dist <= BS_RANGE+1:
#             qual += 0.05*dist - 0.0006*dist**2 
#     return qual

def nodeNetworkQualCalc(node):
    # Store quality for each valid bs
    qualList = []
    for (x, y, z) in BS_POS_LIST:
        dist = distanceCalc(node, (x, y, z))
        if dist <= BS_RANGE+1:
            qdist = 0.43*dist - 0.043*dist**2
            qdist = max(0, min(1, qdist))

            ang = angleCalc([x, y, z], [node[0], node[1], node[2]])
            qang = -3.928571 + 0.09761905*ang - 0.0004761905*ang**2
            qang = max(0, min(1, qang))

            q = (0.5 * qang) + (0.5 * qdist)
            qualList.append(q)

    # Evenlly weighted sum for each quality [0, 1]
    totalQual = 0
    if len(qualList) > 0:
        weight = 1/len(qualList)    
        for qual in qualList:
            totalQual += weight * qual

    return totalQual

# Visualize radiation pattern
# ax = plt.axes(projection='3d')
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')

# for y in range(0, 51):
#     if y == 11 or y == 31:
#         print("BS", y)
#         continue
#     q = nodeNetworkQualCalc((10, y, 10))
#     if q > 0:
#         ax.plot(10, y, 10, marker='o', color='red', alpha=q)
#         print("{:.2f}".format(q))
#         #plt.pause(0.01)

# plt.show()

# Distribution of quality and angle weight at 0-deg y0 = 0.3, y1 = 0.5 y2 = 0.7
# x = np.arange(0, 7, 1)
# y0 = (0.93,0.78,0.44,0.30,0.44,0.78,0.93)
# y1 = (0.95,0.84,0.60,0.50,0.60,0.84,0.95)
# y2 = (0.97,0.91,0.76,0.70,0.76,0.91,0.97)

# plt.plot(x, y0, 'ro-')
# plt.plot(x, y1, 'bo-')
# plt.plot(x, y2, 'yo-')

# plt.show()