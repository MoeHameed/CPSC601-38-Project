from base_station_manager import BaseStationManager as BSM
from air_sim_client import AirSimClient as ASC
import utils

def main():
    # Init base station manager
    bsm = BSM()

    #Init air sim client
    #asc = ASC()

    # for i in range(len(bsm.baseStations)):
    #     asc.spawnObject(bsm.baseStations[i].id, bsm.baseStations[i].size, bsm.baseStations[i].position)

    for i in range(0, 100):
        print([i, i, 0], bsm.baseStations[0].position, utils.distanceCalc([i, i, 0], bsm.baseStations[0].position), bsm.GetNetQuality([i, i, 0]))
    
    # Generate initial path
    # Optimize path
    # Fly path using AirSimClient

if __name__ == "__main__":
    main()