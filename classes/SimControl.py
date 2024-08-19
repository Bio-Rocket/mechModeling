from functions.units import *

import pandas as pd

class SimControl:
    #constants
    timeStep = 0 #the amount of time to increment the simulation by in each time step

    #variables
    currentTime = 0 #current time of the simulation
    
    def __init__(self):
        pass

    def Load(self, dic):
        self.currentTime = convertToSI(dic["startTime"], dic["startTimeUnit"], "time")
        self.timeStep = convertToSI(dic["timeStep"], dic["timeStepUnit"], "time")

    def InitLog(self, log):
        log["simControl.currentTime"] = pd.Series(dtype='float64')

    def Log(self, log):
        log["simControl.currentTime"].iat[-1] = self.currentTime

    def UpdateTime(self):
        self.currentTime += self.timeStep