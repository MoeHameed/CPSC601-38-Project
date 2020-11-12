from base_station_manager import BaseStationManager as BSM
from air_sim_client import AirSimClient as ASC

def main():
    # Init base station manager
    bsm = BSM()

    #Init air sim client
    asc = ASC()

    id = 0

    for x in range(1, 10, 2):
        for y in range(1, 20, 2):
            for z in range(0, 20, 2):
                asc.spawnObject("test" + str(id), [1, 1, 1], [x, y, z])
                id += 1

    # for i in range(len(bsm.baseStations)):
    #     asc.spawnObject(bsm.baseStations[i].id, bsm.baseStations[i].size, bsm.baseStations[i].position)
    
    # Generate initial path
    # Optimize path
    # Fly path using AirSimClient

if __name__ == "__main__":
    main()