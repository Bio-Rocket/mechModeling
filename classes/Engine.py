from classes.OxTank import *
from classes.PressurantTank import *
from classes.EndConditions import *
from classes.SimControl import *
from classes.Parameters import *

import pandas as pd
import numpy as np

class Engine:
    oxTank = "" #instance of class tank
    endConditions = "" #instance of class EndConditions
    simControl = "" #instance of class simControl
    parameters = "" #instance of class parameters
    log_ox = "" #dataFrame tracking simulation values for Oxidizer tank
    log_pressurant = "" #dataFrame tracking simulation values for Pressurant tank

    def __init__(self):
        self.log_ox = pd.DataFrame()
        self.log_pressurant = pd.DataFrame()

    def LoadOx(self, dic):
        tank = "ox"
        self.oxTank = OxTank()
        self.oxTank.Load(dic["oxTank"])

        self.endConditions_ox = EndConditions()
        self.endConditions_ox.Load(dic["endConditions"], tank)

        self.simControl_ox = SimControl()
        self.simControl_ox.Load(dic["simControl"])

        self.parameters_ox = Parameters()
        self.parameters_ox.load(dic["parameters"], tank)

        self.InitLog("ox")

    def LoadPressurant(self, dic):
        tank = "pressurant"
        self.pressurantTank = PressurantTank()
        self.pressurantTank.Load(dic["pressurantTank"])

        self.endConditions_pressurant = EndConditions()
        self.endConditions_pressurant.Load(dic["endConditions"], tank)

        self.simControl_pressurant = SimControl()
        self.simControl_pressurant.Load(dic["simControl"])

        self.parameters_pressurant = Parameters()
        self.parameters_pressurant.load(dic["parameters"], tank)

        self.InitLog("pressurant")

    def InitLog(self, tank):
        if tank == "ox":
            self.oxTank.InitLog(self.log_ox, "engine")
            self.simControl_ox.InitLog(self.log_ox)
        elif tank == "pressurant":
            self.pressurantTank.InitLog(self.log_pressurant, "engine")
            self.simControl_pressurant.InitLog(self.log_pressurant)

    def Log(self, tank):
        if tank == "ox":
            self.log_ox = pd.concat([self.log_ox, pd.DataFrame([{col: None for col in self.log_ox.columns}])], ignore_index=True)
            self.oxTank.Log(self.log_ox, "engine")
            self.simControl_ox.Log(self.log_ox)
        elif tank == "pressurant":
            self.log_pressurant = pd.concat([self.log_pressurant, pd.DataFrame([{col: None for col in self.log_pressurant.columns}])], ignore_index=True)
            self.pressurantTank.Log(self.log_pressurant, "engine")
            self.simControl_pressurant.Log(self.log_pressurant)
    '''
    Summary:
        Drains the oxidizer tank and updates the tank properties at each time step.

    Assuming:
        1. Constant pressure in ullage.
        2. No heat transfer to the tank.
        3. Fixed mass flow rate.
    '''
    def drainOxTank(self):
        print("Running simulation on Oxidizer (", self.oxTank.liquid.fluid,") ...")
        self.Log("ox")
        endReached = False

        while not endReached:
            if self.simControl_ox.currentTime * (1 / self.simControl_ox.timeStep) % 100 == 0:
                print("Current time: " + str(self.simControl_ox.currentTime))
            self.simControl_ox.UpdateTime()
            self.oxTank.RemoveLiquidMass(self.parameters_ox.oxMassFlow, self.simControl_ox.timeStep)
            if self.oxTank.liquid.mass <= self.endConditions_ox.lowOxMass:
                endReached = True
                break

            self.Log("ox")
            
            #set to True to run only once, for testing
            #endReached = True

        self.log_ox.to_csv("log_ox.csv")

    def drainPressurantTank(self):
        print("Running simulation on Pressurant (", self.pressurantTank.gas.fluid,") ...")
        self.Log("pressurant")
        endReached = False

        while not endReached:
            if self.simControl_pressurant.currentTime * (1 / self.simControl_pressurant.timeStep) % 100 == 0:
                print("Current time: " + str(self.simControl_pressurant.currentTime))
            self.simControl_pressurant.UpdateTime()
            self.oxTank.RemoveLiquidMass(self.parameters_pressurant.oxMassFlow, self.simControl_pressurant.timeStep)
            if self.oxTank.liquid.mass <= self.endConditions_pressurant.lowOxMass:
                endReached = True
                break

            self.Log("pressurant")
            
            #set to True to run only once, for testing
            #endReached = True

        self.log_pressurant.to_csv("log_pressurant.csv")