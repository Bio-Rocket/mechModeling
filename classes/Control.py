from functions.units import *

import pandas as pd

class Control:
    #constant
    name = 0 #The name of the controller
    openDelay = 0 #The delay between energizing coil and fully open valve, in s.
    closeDelay = 0 #The delay between de-energizing coil and fully closed valve, in s.

    lowThreshold = 0 #The pressure at which to open the valve, in Pa
    setPoint = 0 #The ideal pressure for the system to operate at, in Pa
    highThreshold = 0 #The pressure at which to close the valve, in Pa

    #variables
    opened = False #The state of the valve, True or False
    energized = False #The state of the coil, True or False

    timeCoilCycled = 0 #The time at which the state of the coil last changed, in s
    timeValveCycled = 0 #The time at which the state of the valve last changed, in s

    def __init__(self):
        pass

    def Load(self, dic):
        self.name = dic["name"]
        self.openDelay = convertToSI(dic["openDelay"], dic["openDelayUnit"], "time")
        self.closeDelay = convertToSI(dic["closeDelay"], dic["closeDelayUnit"], "time")
        self.lowThreshold = convertToSI(dic["lowThreshold"], dic["lowThresholdUnit"], "pressure")
        self.highThreshold = convertToSI(dic["highThreshold"], dic["highThresholdUnit"], "pressure")
        self.setPoint = convertToSI(dic["setPoint"], dic["setPointUnit"], "pressure")

    def InitLog(self, log, name):
        name += "." + self.name
        log[name + ".opened"] = pd.Series(dtype='bool')
        log[name + ".energized"] = pd.Series(dtype='bool')
        log[name + ".timeCoilCycled"] = pd.Series(dtype='bool')
        log[name + ".timeValveCycled"] = pd.Series(dtype='bool')

    def Log(self, log, name):
        name += "." + self.name
        log[name +".opened"].iat[-1] = str(self.opened)
        log[name +".energized"].iat[-1] = str(self.energized)
        log[name +".timeCoilCycled"].iat[-1] = str(self.timeCoilCycled)
        log[name +".timeValveCycled"].iat[-1] = str(self.timeValveCycled)

    def DetermineState(self, oxPressure, currentTime):
        
        #in this case, the valve needs to be opened
        if oxPressure < self.lowThreshold:

            #the valve is still closed, need to open it.
            if not self.opened:
                
                #If the valve is being opened already, keep opening it, but check if it has opened fully.
                if self.energized:
                    if currentTime - self.timeCoilCycled >= self.openDelay:
                        self.opened = True
                        self.timeValveCycled = currentTime

                #The pressure is below threshold, the valve is not yet open, and not yet energized, therefore, energize it.
                else:
                    self.energized = True
                    self.timeCoilCycled = currentTime

        #in this case, the valve needs to be closed. 
        if oxPressure > self.highThreshold:

            #if the valve is still open, need to close it. 
            if self.opened:

                #if the valve is open and still energized, de-energize it
                if self.energized:
                    self.energized = False
                    self.timeCoilCycle = currentTime

                #if the valve is being closed already, continue closing it, but check if it has closed fully.
                else:
                    if currentTime - self.timeCoilCycle > self.closeDelay:
                        self.open = False
                        self.timeValveCycled = currentTime