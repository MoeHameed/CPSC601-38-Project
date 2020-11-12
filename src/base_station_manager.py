from base_station import BaseStation
import consts

class BaseStationManager:
    def __init__(self):
        self.baseStations = []

        for i in range(consts.BS_NUM):
            self.baseStations.append(BaseStation(consts.BS_POS_LIST[i]))