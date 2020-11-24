from air_sim_client import AirSimClient as ASC
from path_planner import PathPlanner
import utils
import matplotlib.pyplot as plt
import vg

simulate = True

minQuality = 0.6949

START_POS = (1, 1, 1)
END_POS = (35, 48, 22)

BS_POS_LIST_A = [(25, 25, 0), (10, 45, 0), (15, 55, 0)]
BS_POS_LIST_B = []
BS_POS_LIST_C = []

def main():
    utils.BS_POS_LIST = BS_POS_LIST_A

    # Generate initial optimal-greedy path
    print("Generating initial path . . .")
    initialPath = PathPlanner().search(START_POS, END_POS)
    print("Initial path average quality:", utils.calcPathAvgQual(initialPath))
    print("Initial path total distance:", utils.calcPathDist(initialPath))
    
    # Optimize path
    print("Generating smooth path . . .")
    cornerPoints = utils.getCornerPoints(initialPath)
    smoothQual, smoothPath, bestQual, _ = utils.threshSmoothPath(cornerPoints, minQuality)

    # Check if optimization was possible
    if len(smoothPath) < 2:
        print("Smooth path not found with minimum quality of {}. Maximum quality found is {:.4f}".format(minQuality, bestQual))
        return
    
    print("Smooth path average quality:", smoothQual)
    print("Smooth path total distance:", utils.calcPathDist(smoothPath))
    utils.plotPath(smoothPath)
    
    if simulate:
        print("Simulating smooth path in AirSim . . .")

        # Init air sim client
        asc = ASC()

        # Spawn base stations
        i = 0
        for (x, y, z) in utils.BS_POS_LIST:
            asc.spawnObject(i, utils.BS_SIZE, (x, y, z))
            i += 1

        # Fly path using AirSimClient
        asc.flyPath(smoothPath)

        # Evaluate path through airsim

if __name__ == "__main__":
    main()