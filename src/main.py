from base_station_manager import BaseStationManager

def main():
    # Init base station manager
    baseStationManager = BaseStationManager(5)

    for i in range(len(baseStationManager.baseStations)):
        print(baseStationManager.baseStations[i].networkQuality)

    # Generate initial path
    # Optimize path
    # Fly path using AirSimClient

if __name__ == "__main__":
    main()