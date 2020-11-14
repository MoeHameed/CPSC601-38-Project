from base_station_manager import BaseStationManager as BSM
from air_sim_client import AirSimClient as ASC
from path_planner import PathPlanner
import utils


def main():
    # Init base station manager
    bsm = BSM()

    # Init air sim client
    # asc = ASC()

    # Spawn base stations
    # for i in range(len(bsm.baseStations)):
    #     asc.spawnObject(bsm.baseStations[i].id, bsm.baseStations[i].size, bsm.baseStations[i].position)
    
    # Generate initial path
    initialPath = PathPlanner(True, True).search(utils.START_POS, utils.END_POS)
    
    # Optimize path
    # Fly path using AirSimClient
    # Evaluate path

if __name__ == "__main__":
    main()



# Test distance and net quality
# for i in range(0, 100):
#     print([i, i, 0], bsm.baseStations[0].position, utils.distanceCalc([i, i, 0], bsm.baseStations[0].position), bsm.GetNetQuality([i, i, 0]))