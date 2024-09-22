from classes.OxTank import *
from classes.PressTank import *
from classes.EndConditions import *
from classes.SimControl import *
from classes.Parameters import *

import pandas as pd
import numpy as np

class Engine:
    oxTank = "" #instance of class Oxtank
    pressTank = '' #instance of class PressTank
    endConditions = "" #instance of class EndConditions
    simControl = "" #instance of class simControl
    parameters = "" #instance of class parameters
    log = "" #dataFrame tracking simulation values

    def __init__(self):
        self.log = pd.DataFrame()

    def Load(self, dic):
        self.oxTank = OxTank()
        self.oxTank.Load(dic["oxTank"])

        self.pressTank = PressTank()
        self.pressTank.Load(dic["pressTank"])

        self.endConditions = EndConditions()
        self.endConditions.Load(dic["endConditions"])

        self.simControl = SimControl()
        self.simControl.Load(dic["simControl"])

        self.parameters = Parameters()
        self.parameters.load(dic["parameters"])

        self.InitLog()

    def InitLog(self):
        self.oxTank.InitLog(self.log, "engine")
        self.pressTank.InitLog(self.log, "engine")
        self.simControl.InitLog(self.log)

    def Log(self):
        self.log = pd.concat([self.log, pd.DataFrame([{col: None for col in self.log.columns}])], ignore_index=True)
        self.oxTank.Log(self.log, "engine")
        self.pressTank.Log(self.log, "engine")
        self.simControl.Log(self.log)

    '''
    Summary:
        Drains the oxidizer tank and updates the tank properties at each time step.

    Assuming:
        1. Constant pressure in ullage.
        2. No heat transfer to the tank.
        3. Fixed mass flow rate.
    '''
    def drainTanks(self):
        print("Running simulation...")

        self.pressTank.CalcGassMassFlow(self.parameters.oxMassFlow, self.oxTank.liquid)

        self.Log()
        endReached = False

        while not endReached:

            if self.simControl.currentTime * int(1 / self.simControl.timeStep) % 100 == 0:
                print("Current time: " + str(self.simControl.currentTime))

            self.simControl.UpdateTime()
            self.oxTank.RemoveLiquidMass(self.parameters.oxMassFlow, self.simControl.timeStep)

            self.pressTank.RemoveGasMass(self.parameters.oxMassFlow, self.simControl.timeStep, self.oxTank.liquid)

            if self.oxTank.liquid.mass <= self.endConditions.lowOxMass:
                endReached = True
                break

            self.Log()
            
            #set to True to run only once, for testing
            #endReached = True

        self.log.to_csv("log.csv")