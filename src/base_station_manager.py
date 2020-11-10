from base_station import BaseStation

class BaseStationManager:
    def __init__(self, numBaseStations):
        self.baseStations = []
        for _ in range(numBaseStations):
            pos = [1, 2, 3]
            self.baseStations.append(BaseStation(pos))