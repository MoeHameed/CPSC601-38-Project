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
BS_SIZE = [1, 1, 25]
BS_NUM = 6
BS_POS_LIST = [
    [100, 100, 0],
    [200, 100, 0],
    [300, 100, 0],
    [100, 200, 0],
    [200, 200, 0],
    [300, 200, 0]]

# Path consts
START_POS = (1, 1, 1)
END_POS = (15, 40, 25)

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
    c = b - a   # calc difference vector
    z = [0, 0, 1] # unit vector
    return vg.angle(c, z)
    
    # Used to visualize
    # data = [A, B]
    # x, y, z = zip(*data)
    # ax = plt.axes(projection='3d')
    # ax.plot3D(x, y, z, 'ro-')
    # ax.text(B[0], B[1], B[2], "{:.2f}".format(angle))
    # plt.pause(0.05)