class BaseStation:
    id = -1

    # TODO: Bandwidth, Throughput, PacketLoss, Latency, Jitter, AntennaGain, NetworkQuality
    def __init__(self, position):
        BaseStation.id += 1
        self.id = BaseStation.id
        self.position = position
        self.size = [1, 1, 35]
        self.networkQuality = 0.8
    
    def SimulateNetworkQuality(self):
        # TODO: Generate network values
        self.networkQuality = 0.8