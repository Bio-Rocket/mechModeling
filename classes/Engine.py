from classes.OxTank import *
from classes.PressTank import *
from classes.EndConditions import *
from classes.SimControl import *
from classes.Parameters import *
from classes.FlowLine import *
from classes.Orifice import *

import pandas as pd
import numpy as np

class Engine:
    oxTank = "" #instance of class Oxtank
    pressTank = "" #instance of class PressTank
    nitrousPressurantValve = "" #instance of class Orifice

    endConditions = "" #instance of class EndConditions
    simControl = "" #instance of class simControl
    parameters = "" #instance of class parameters
    log = "" #dataFrame tracking simulation values for Oxidizer tank

    def __init__(self):
        self.log = pd.DataFrame()

    def Load(self, dic):
        self.oxTank = OxTank()
        self.oxTank.Load(dic["oxTank"])

        self.pressTank = PressTank()
        self.pressTank.Load(dic["pressTank"])

        self.nitrousPressurantValve = Orifice()
        self.nitrousPressurantValve.Load(dic["nitrousPressurantValve"])
        self.nitrousPressurantValve.inlet = self.pressTank.gas
        self.nitrousPressurantValve.outlet = self.oxTank.gas
        self.nitrousPressurantValve.initial = self.pressTank.initial

        self.endConditions = EndConditions()
        self.endConditions.Load(dic["endConditions"])

        self.simControl = SimControl()
        self.simControl.Load(dic["simControl"])

        self.parameters = Parameters()
        self.parameters.load(dic["parameters"])

        self.InitLog()

    def InitLog(self):
        self.simControl.InitLog(self.log)
        self.oxTank.InitLog(self.log, "engine")
        self.pressTank.InitLog(self.log, "engine")
        self.nitrousPressurantValve.InitLog(self.log, "engine")

    def Log(self):
        self.log = pd.concat([self.log, pd.DataFrame([{col: None for col in self.log.columns}])], ignore_index=True)
        
        self.simControl.Log(self.log)
        self.oxTank.Log(self.log, "engine")
        self.nitrousPressurantValve.Log(self.log, "engine")
        self.pressTank.Log(self.log, "engine")

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
        self.nitrousPressurantValve.CalcMassFlow(self.simControl.currentTime)

        self.Log()
        endReached = False

        while not endReached:

            self.nitrousPressurantValve.CalcMassFlow(self.simControl.currentTime)

            if int( self.simControl.currentTime * (1 / self.simControl.timeStep)) % 100 == 0:
                print("Current time: %.3f" % self.simControl.currentTime)

            self.simControl.UpdateTime()

            if self.simControl.currentTime > self.endConditions.endTime:
                endReached = True
                print("Simulation terminated. Reached end time.")
                break

            self.oxTank.liquid.RemoveMass(self.parameters.oxMassFlow, self.simControl.timeStep)

            if self.oxTank.liquid.mass <= self.endConditions.lowOxMass:
                endReached = True
                print("Simulation terminated. Ran out of oxidizer.")
                break

            self.oxTank.liquid.RemoveEnergy(self.parameters.oxMassFlow, self.simControl.timeStep)
            
            #assuming pressure stays constant (due to active pressure control), update other properties
            self.oxTank.liquid.SetIntrinsicProperties("pressure", self.oxTank.liquid.pressure, "internalEnergy", self.oxTank.liquid.internalEnergy)
            self.oxTank.liquid.SetExtrinsicProperties("mass", self.oxTank.liquid.mass)

            self.pressTank.CalcGassMassFlow(self.parameters.oxMassFlow, self.oxTank.liquid)
            self.pressTank.gas.RemoveMass(self.pressTank.pressurantMassFlowRate, self.simControl.timeStep)

            if self.pressTank.gas.mass <= self.endConditions.lowPressurantMass:
                endReached = True
                print("Simulation terminated. Ran out of pressurant.")
                break

            self.pressTank.gas.RemoveEnergy(self.pressTank.pressurantMassFlowRate, self.simControl.timeStep)
            
            #using constant volume, new mass, and new internal energy, find other properties
            self.pressTank.gas.SetIntrinsicProperties("density", self.pressTank.gas.mass/self.pressTank.gas.volume, "internalEnergy", self.pressTank.gas.internalEnergy)
            
            #update the log
            self.Log()
            
            #set to True to run only once, for testing
            #endReached = True

        self.log.to_csv("log.csv")
    
    '''
        Summary:
            Combines the pressurant tank discharge, nitrous tank discharge, control logic, and propellant mass flow models
            to generate the properties vs. time of the pressurant tank and the nitrous tank.

        Assuming:
            1. Liquid - gas interface between nitrous and nitrogen acts as a piston.
                a) No heat transfer across interface.
                b) No mass transfer across interface.
            2. No heat transfer to the tanks.
            3. Fixed nitrous mass flow rate.
    '''
    def RunSim(self):
        print("Running simulation...")

        self.nitrousPressurantValve.CalcMassFlow()

        self.Log()
        endReached = False

        while not endReached:

            self.nitrousPressurantValve.CalcMassFlow()

            #print sim progress to terminal every 100 timeSteps.
            if int( self.simControl.currentTime * (1 / self.simControl.timeStep)) % 100 == 0:
                print("Current time: %.3f" % self.simControl.currentTime)

            #start the next timeStep
            self.simControl.UpdateTime()

            #check if the sim has ended due to reaching the limit timeStep.
            if self.simControl.currentTime > self.endConditions.endTime:
                endReached = True
                print("Simulation terminated. Reached end time.")
                break

            self.oxTank.RemoveLiquidMass(self.parameters.oxMassFlow, self.simControl.timeStep)

            if self.oxTank.liquid.mass <= self.endConditions.lowOxMass:
                endReached = True
                print("Simulation terminated. Ran out of oxidizer.")
                break

            self.oxTank.RemoveLiquidEnergy(self.parameters.oxMassFlow, self.simControl.timeStep)

            self.pressTank.RemoveGasMass(self.parameters.oxMassFlow, self.simControl.timeStep, self.oxTank.liquid)

            if self.pressTank.gas.mass <= self.endConditions.lowPressurantMass:
                endReached = True
                print("Simulation terminated. Ran out of pressurant.")
                break

            self.pressTank.RemoveGasEnergy(self.simControl.timeStep)

            self.Log()
            
            #set to True to run only once, for testing
            #endReached = True

        self.log.to_csv("log.csv")