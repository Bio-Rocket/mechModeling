from functions.units import *

class EndConditions:

    lowOxMass = 0 #oxidizer mass at which to terminate the simulation.
    endTime = 0 #burn time at which to terminate the simulation.

    def __init__(self):
        pass

    def Load(self, dic):
        self.lowOxMass = convertToSI(dic["lowOxMass"], dic["lowOxMassUnit"], "mass")
        self.endTime = convertToSI(dic["endTime"], dic["endTimeUnit"], "time")