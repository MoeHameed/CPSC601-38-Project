from base_station_manager import BaseStationManager as BSM
from air_sim_client import AirSimClient as ASC
from path_planner import PathPlanner
import utils
import matplotlib.pyplot as plt


def main():
    # Init base station manager
    # bsm = BSM()

    # Generate initial path
    initialPath = PathPlanner().search(utils.START_POS, utils.END_POS)

    qual = 0
    for node in initialPath:
        q = utils.nodeNetworkQualCalc(node)
        print(node, q)
        qual += q
    print("avg", qual, len(initialPath), qual/len(initialPath))
        

    
    # Optimize path
    
    # Init air sim client
    # asc = ASC()

    # Spawn base stations
    # for i in range(len(bsm.baseStations)):
    #     asc.spawnObject(bsm.baseStations[i].id, bsm.baseStations[i].size, bsm.baseStations[i].position)

    # Fly path using AirSimClient

    # Evaluate path


if __name__ == "__main__":
    main()



# Test distance and net quality
# for i in range(0, 100):
#     print([i, i, 0], bsm.baseStations[0].position, utils.distanceCalc([i, i, 0], bsm.baseStations[0].position), bsm.GetNetQuality([i, i, 0]))