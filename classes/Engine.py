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

            m = self.oxTank.liquid.RemoveMass(self.parameters.oxMassFlow, self.simControl.timeStep)

            if m <= self.endConditions.lowOxMass:
                endReached = True
                print("Simulation terminated. Ran out of oxidizer.")
                break

            u = self.oxTank.liquid.RemoveEnergy(self.parameters.oxMassFlow, self.simControl.timeStep)
            
            #assuming pressure stays constant (due to active pressure control), update other properties
            self.oxTank.liquid.SetIntrinsicProperties("pressure", self.oxTank.liquid.pressure, "internalEnergy", u)
            self.oxTank.liquid.SetExtrinsicProperties("mass", m)

            self.pressTank.CalcGassMassFlow(self.parameters.oxMassFlow, self.oxTank.liquid)
            m = self.pressTank.gas.RemoveMass(self.pressTank.pressurantMassFlowRate, self.simControl.timeStep)
            self.pressTank.gas.SetExtrinsicProperties("mass", m)

            if m <= self.endConditions.lowPressurantMass:
                endReached = True
                print("Simulation terminated. Ran out of pressurant.")
                break

            u = self.pressTank.gas.RemoveEnergy(self.pressTank.pressurantMassFlowRate, self.simControl.timeStep)
            
            #using constant volume, new mass, and new internal energy, find other properties
            self.pressTank.gas.SetIntrinsicProperties("density", self.pressTank.gas.mass/self.pressTank.gas.volume, "internalEnergy", u)
            
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
    def runSim(self):
        print("Running simulation...")

        self.nitrousPressurantValve.CalcMassFlow(self.simControl.currentTime)

        self.Log()
        endReached = False

        while not endReached:
            
            #calculate the mass flow rate through the pressurisation valve, taking into account control logic 
            self.nitrousPressurantValve.CalcMassFlow(self.simControl.currentTime)

            #print sim status to console every 100 time steps.
            if int( self.simControl.currentTime * (1 / self.simControl.timeStep)) % 100 == 0:
                print("Current time: %.3f" % self.simControl.currentTime)

            #move to the next time step in the simulation.
            self.simControl.UpdateTime()

            #check if the simulation has timed out.
            if self.simControl.currentTime > self.endConditions.endTime:
                endReached = True
                print("Simulation terminated. Reached end time.")
                break

            #calculate the liquid mass at the next timeStep. 
            m = self.oxTank.liquid.RemoveMass(self.parameters.oxMassFlow, self.simControl.timeStep)

            #check if the oxidizer tank has run out of liquid.
            if m <= self.endConditions.lowOxMass:
                endReached = True
                print("Simulation terminated. Ran out of oxidizer.")
                break

            #calculate the specific internal energy at the new timeStep by enforcing conservation of energy
            u = self.oxTank.liquid.RemoveEnergy(self.parameters.oxMassFlow, self.simControl.timeStep)
            
            #Start iterative solver to find nitrous volume

            #The minimum volume nitrous could occupy is given by the case where the pressure of nitrous is equal to the nitrogen tank pressure
            a = m / cp.PropsSI('D', 'U', self.oxTank.liquid.internalEnergy, 'P', self.pressTank.gas.pressure, self.oxTank.liquid.fluid)

            #The maximum volume nitrous could occupy is given by the case where the pressure of nitrogen is equal to the nitrogen tank pressure.
            b = self.oxTank.volume - ( ( self.oxTank.gas.mass * self.oxTank.gas.R * self.oxTank.gas.temperature ) / self.pressTank.gas.pressure )
            c = (a + b) / 2

            def Pressure(VNOS):
                PN2 = self.oxTank.gas.mass * self.oxTank.gas.R * self.oxTank.gas.temperature / (self.oxTank.volume - VNOS)
                PNOS = cp.PropsSI('P', 'U', self.oxTank.liquid.internalEnergy, 'D', m / VNOS, self.oxTank.liquid.fluid)
                return PN2 - PNOS

            iterations = 0
            while True:
                iterations += 1
                fa = Pressure(a)
                fc = Pressure(c)

                if fa * fc < 0:
                    b = c

                else:
                    a = c

                c = (a + b) / 2

                if iterations > 100:
                    break

                if abs(Pressure(a) - Pressure(b)) < 70:
                    break

            rho = m / c

            #update the intrinsic properties of the liquid phae in the oxidizer tank using the new internal energy and density
            self.oxTank.liquid.SetIntrinsicProperties("density", rho, "internalEnergy", u)

            #update the extrinsic properties of the liquid phase in the oxidizer tank using the new mass and the above determined density.
            self.oxTank.liquid.SetExtrinsicProperties("mass", m)

            #find the volume occupied by the gas phase in the oxidizer tank
            v = self.oxTank.volume - self.oxTank.liquid.volume

            #find the pressure and temperature using isentropic expansion
            P, T = self.oxTank.gas.IstentropicVolumeChange(v)
            
            #update the intrinsic properties of the gas phase in the oxidizer tank using the pressure and temperature found from isentropic expansion
            self.oxTank.gas.SetIntrinsicProperties("temperature", T, "pressure", P)

            #update the extrinsic properties of the gas phase in the oxidizer tank using the new volume
            self.oxTank.gas.SetExtrinsicProperties("volume", v)

            #!!!!!!!!
            #assuming pressure stays constant (due to active pressure control), update other properties
            #self.oxTank.liquid.SetIntrinsicProperties("pressure", self.oxTank.liquid.pressure, "internalEnergy", u)
            #!!!!!!!!



            if self.nitrousPressurantValve.controller.opened:
                print("Simulation terminated! Pressurant valve opened.")
                break
                #TODO: Add N2 mass and energy to the gas phase in the oxidizer tank.

                #calculate the amount of mass removed from the pressurant tank
                m = self.pressTank.gas.RemoveMass(self.nitrousPressurantValve.massFlowRate, self.simControl.timeStep)

                if m <= self.endConditions.lowPressurantMass:
                    endReached = True
                    print("Simulation terminated. Ran out of pressurant.")
                    break

                if self.pressTank.gas.pressure <= self.oxTank.liquid.pressure:
                    endReached = True
                    print("Simulation terminated. Pressurant pressure dropped below oxidizer tank pressure.")
                    break

                u = self.pressTank.gas.RemoveEnergy(self.pressTank.pressurantMassFlowRate, self.simControl.timeStep)
                
                #update the intrinsic properties using the fixed volume, the new mass, and the new internal energy
                self.pressTank.gas.SetIntrinsicProperties("density", m/self.pressTank.gas.volume, "internalEnergy", u)
                
                #update the extrinsic properties of the gas in the pressurant tank using the new mass and the density.
                self.pressTank.SetExtrinsicProperties("mass", m)

            #update the log
            self.Log()
            
            #set to True to run only once, for testing
            #endReached = True

        self.log.to_csv("log2.csv")