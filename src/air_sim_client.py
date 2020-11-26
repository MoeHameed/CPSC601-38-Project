import airsim
import pprint
import time

class AirSimClient:
    def __init__(self):
        self.spawnedObjs = []
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()

    def spawnObject(self, name, size, position):
        objPose = airsim.Pose()
        x = position[0] + (0.5 * (size[0] - 1))
        y = position[1] + (0.5 * (size[1] - 1))
        z = position[2] + (0.5 * (size[2] - 1))
        objPose.position = airsim.Vector3r(x, y, -z)

        objSize = airsim.Vector3r(size[0], size[1], size[2])

        objName = "SimObject_" + str(name)

        self.client.simSpawnObject(objName, "mycube", objPose, objSize)
        self.spawnedObjs.append(objName)
        
        print("Spawned: ", objName)

    def flyPath(self, path):
        self.client.enableApiControl(True)
        self.client.armDisarm(True)
        self.client.takeoffAsync().join()

        p = []
        for (x, y, z) in path:
            p.append(airsim.Vector3r(x, y, -z))

        self.client.simPlotLineStrip(p, [1, 0, 0, 1], 15, 100000, True)

        print("Flying along path . . .")
        self.client.moveOnPathAsync(p, 3, 3e38, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False, 0), 1, 0).join()
        print("Done!")

        self.client.hoverAsync().join()
        print("Drone is now hovering . . . ")


# def updateObject(name, topleft):
#     n = "SimObject_" + str(name)
#     p = airsim.Pose()
#     p.position = airsim.Vector3r(topleft[0], topleft[1], (topleft[2]-1.5)*-1)
#     client.simSetObjectPose(n, p)
#     print("Updated: ", name)