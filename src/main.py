from air_sim_client import AirSimClient as ASC
from path_planner import PathPlanner
import utils
import matplotlib.pyplot as plt
import vg

simulate = False

minQuality = 0.80

START_POS = (15, 15, 18)
END_POS = (50, 75, 27)

BS_POS_LIST_A = [(25, 25, 0), (25, 85, 0), (85, 25, 0), (85, 85, 0)]
BS_POS_LIST_B = []
BS_POS_LIST_C = []

def main():
    utils.BS_POS_LIST = BS_POS_LIST_A

    print("Generating distance based path . . .")
    distPath = PathPlanner(False).search(START_POS, END_POS)
    print("Distance based path average quality: {:.4f}".format(utils.calcPathAvgQual(distPath)))
    print("Distance based path total distance: {:.2f} meters".format(utils.calcPathDist(distPath)))

    # Generate initial optimal-greedy path
    print("Generating initial path . . .")
    initialPath = PathPlanner().search(START_POS, END_POS)
    print("Initial path average quality: {:.4f}".format(utils.calcPathAvgQual(initialPath)))
    print("Initial path total distance: {:.2f} meters".format(utils.calcPathDist(initialPath)))
    
    # Optimize path
    print("Generating smooth path . . .")
    cornerPoints = utils.getCornerPoints(initialPath)
    smoothQual, smoothPath, bestQual, _ = utils.threshSmoothPath(cornerPoints, minQuality)

    # Check if optimization was possible
    if len(smoothPath) < 2:
        print("Smooth path not found with minimum quality of {}. Maximum quality found is {:.4f}".format(minQuality, bestQual))
        return
    
    print("Smooth path average quality: {:.4f}".format(smoothQual))
    print("Smooth path total distance: {:.2f} meters".format(utils.calcPathDist(smoothPath)))
    utils.plotPath([smoothPath])
    
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