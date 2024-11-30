from classes.OxTank import *
from classes.FuelTank import *
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
    fuelTank = "" #instance of class fuelTank
    nitrousPressurantValve = "" #instance of class Orifice

    pressurantFlowRate = "" #The mass flow rate of pressurant

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

        self.fuelTank = FuelTank()
        self.fuelTank.Load(dic["fuelTank"])

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
        self.fuelTank.InitLog(self.log, "engine")
        self.nitrousPressurantValve.InitLog(self.log, "engine")

        self.log["engine.pressurantFlowRate"] = pd.Series(dtype='float64')

    def Log(self):
        self.log = pd.concat([self.log, pd.DataFrame([{col: None for col in self.log.columns}])], ignore_index=True)
        
        self.simControl.Log(self.log)
        self.oxTank.Log(self.log, "engine")
        self.fuelTank.Log(self.log, "engine")
        self.nitrousPressurantValve.Log(self.log, "engine")
        self.pressTank.Log(self.log, "engine")

        self.log["engine.pressurantFlowRate"].iat[-1] = self.pressurantFlowRate

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
            if int( self.simControl.currentTime * (1 / self.simControl.timeStep)) % 50 == 0:
                print("Current time: %.3f" % self.simControl.currentTime)
                self.log.to_csv("log.csv")

            #move to the next time step in the simulation.
            self.simControl.UpdateTime()

            #check if the simulation has timed out.
            if self.simControl.currentTime > self.endConditions.endTime:
                endReached = True
                print("Simulation terminated. Reached end time.")
                break

            '''
            ################################################################
            #####################DRAINING OXIDIZER TANK#####################
            ################################################################
            '''

            #calculate the liquid mass at the next timeStep. 
            m = self.oxTank.liquid.RemoveMass(self.parameters.oxMassFlow, self.simControl.timeStep)

            #check if the oxidizer tank has run out of liquid.
            if m <= self.endConditions.lowOxMass:
                endReached = True
                print("Simulation terminated. Ran out of oxidizer.")
                break

            #calculate the specific internal energy at the new timeStep by enforcing conservation of energy
            u = self.oxTank.liquid.RemoveEnergy(self.parameters.oxMassFlow, self.simControl.timeStep)
            
            #Start iterative solver to find nitrous volume given a new liquid nitrous mass
            def RemoveOxDensity(mOx):
                #Use bisection algorithm
                
                #The minimum volume nitrous could occupy is given by the case where the pressure of nitrous is equal to the nitrogen tank pressure
                a = mOx / cp.PropsSI('D', 'U', self.oxTank.liquid.internalEnergy, 'P', self.pressTank.gas.pressure, self.oxTank.liquid.fluid)

                #The maximum volume nitrous could occupy is given by the case where the pressure of nitrogen is equal to the nitrogen tank pressure.
                b = self.oxTank.volume - ( ( self.oxTank.gas.mass * self.oxTank.gas.R * self.oxTank.gas.temperature ) / self.pressTank.gas.pressure )
                c = (a + b) / 2

                #assuming a volume occupied by the liquid nitrous phase, return the difference between nitrogen and nitrous prressures.
                def Pressure(VNOS):
                    PN2, TN2 = self.oxTank.gas.IsentropicVolumeChange(self.oxTank.volume - VNOS)
                    PNOS = cp.PropsSI('P', 'U', self.oxTank.liquid.internalEnergy, 'D', mOx / VNOS, self.oxTank.liquid.fluid)
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

                    if abs(Pressure(a) - Pressure(b)) < 70:
                        break

                PN2, TN2 = self.oxTank.gas.IsentropicVolumeChange(self.oxTank.volume - c)
                return mOx / c, PN2

            rho, P = RemoveOxDensity(m)

            #update the intrinsic properties of the liquid phase in the oxidizer tank using the new internal energy and density
            self.oxTank.liquid.SetIntrinsicProperties("density", rho, "pressure", P)

            #update the extrinsic properties of the liquid phase in the oxidizer tank using the new mass and the above determined density.
            self.oxTank.liquid.SetExtrinsicProperties("mass", m)

            #find the volume occupied by the gas phase in the oxidizer tank
            v = self.oxTank.volume - self.oxTank.liquid.volume

            #find the pressure and temperature using isentropic expansion
            P, T = self.oxTank.gas.IsentropicVolumeChange(v)
            
            #update the intrinsic properties of the gas phase in the oxidizer tank using the pressure and temperature found from isentropic expansion
            self.oxTank.gas.SetIntrinsicProperties("temperature", T, "pressure", P)

            #update the extrinsic properties of the gas phase in the oxidizer tank using the new volume
            self.oxTank.gas.SetExtrinsicProperties("mass", self.oxTank.gas.mass)

            if self.nitrousPressurantValve.controller.opened:

                '''
                #################################################################
                ######################FILLING OXIDIZER TANK######################
                #################################################################
                '''

                #calculate the mass of the gas phase in the oxidizer tank at the next time step
                mGas = self.oxTank.gas.AddMass(self.nitrousPressurantValve.massFlowRate, self.simControl.timeStep)
                
                #Start iterative solver to find gas volume given a new gas phase mass
                def AddGasDensity(mGas):
                    #Use bisection algorithm
                    
                    #The minimum volume nitrous could occupy is given by the case where the pressure of nitrous is equal to the nitrogen tank pressure
                    a = self.oxTank.liquid.mass / cp.PropsSI('D', 'U', self.oxTank.liquid.internalEnergy, 'P', self.pressTank.gas.pressure, self.oxTank.liquid.fluid)

                    #The maximum volume nitrous could occupy is given by the case where the pressure of nitrogen is equal to the nitrogen tank pressure.
                    b = self.oxTank.volume - ( ( self.oxTank.gas.mass * self.oxTank.gas.R * self.oxTank.gas.temperature ) / self.pressTank.gas.pressure )
                    c = (a + b) / 2

                    #assuming a volume occupied by the liquid nitrous phase, return the difference between nitrogen and nitrous pressures.
                    def Pressure(VNOS):
                        PN2 = mGas * self.oxTank.gas.R * self.oxTank.gas.temperature / (self.oxTank.volume - VNOS)
                        PNOS = cp.PropsSI('P', 'U', self.oxTank.liquid.internalEnergy, 'D', self.oxTank.liquid.mass / VNOS, self.oxTank.liquid.fluid)
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

                        if abs(Pressure(a) - Pressure(b)) < 50:
                            break

                    return self.oxTank.liquid.mass / c, mGas * self.oxTank.gas.R * self.oxTank.gas.temperature / (self.oxTank.volume - c)

                #find the new density of the liquid phase in the oxidizer tank
                rhoNOS, P = AddGasDensity(mGas)

                #update the intrinsic properties of the liquid phase in the oxidizer tank using the new internal energy and density
                self.oxTank.liquid.SetIntrinsicProperties("density", rhoNOS, "pressure", P)

                #update the extrinsic properties of the liquid phase in the oxidizer tank using the new mass and the above determined density.
                self.oxTank.liquid.SetExtrinsicProperties("mass", self.oxTank.liquid.mass)

                #This seemed like a more correct way to do it, but it gave really weird results.
                #find the temperature that the pressurant reaches when it expands to the pressure of the oxidizer tank
                T = self.pressTank.gas.IsentropicPressureChange(P)

                #find the specific enthalpy at this state
                H = cp.PropsSI('H', 'P', P, 'T', T, self.pressTank.gas.fluid)

                #use mixing to find the new enthalpy of the phase
                u = self.oxTank.gas.AddEnergy(self.nitrousPressurantValve.massFlowRate, self.simControl.timeStep, H)

                #find the volume occupied by the gas phase
                v = self.oxTank.volume - self.oxTank.liquid.volume

                #update the intrinsic properties of the gas phase in the oxTank using the new specific enthalpy and the new density
                self.oxTank.gas.SetIntrinsicProperties("density", mGas / v, "pressure", P)

                #update the extrinsic properties of the gas phase in the oxTank using the new mass
                self.oxTank.gas.SetExtrinsicProperties("mass", mGas)

                '''
                ################################################################
                ####################DRAINING PRESSURANT TANK####################
                ################################################################
                '''

                #calculate the amount of mass removed from the pressurant tank
                mPress = self.pressTank.gas.RemoveMass(self.nitrousPressurantValve.massFlowRate, self.simControl.timeStep)

                if mPress <= self.endConditions.lowPressurantMass:
                    endReached = True
                    print("Simulation terminated. Ran out of pressurant.")
                    break

                if self.pressTank.gas.pressure <= self.oxTank.liquid.pressure:
                    endReached = True
                    print("Simulation terminated. Pressurant pressure dropped below oxidizer tank pressure.")
                    break

                u = self.pressTank.gas.RemoveEnergy(self.nitrousPressurantValve.massFlowRate, self.simControl.timeStep)
                
                #update the intrinsic properties using the fixed volume, the new mass, and the new internal energy
                self.pressTank.gas.SetIntrinsicProperties("density", mPress/self.pressTank.gas.volume, "internalEnergy", u)
                
                #update the extrinsic properties of the gas in the pressurant tank using the new mass and the density.
                self.pressTank.gas.SetExtrinsicProperties("mass", mPress)

            #update the log
            self.Log()
            
            #set to True to run only once, for testing
            #endReached = True

        self.log.to_csv("log.csv")

    def RegulatorBlowDown(self):
        print("Running Simulation...")

        self.Log()

        endReached = False

        while not endReached:

            #update the time
            self.simControl.UpdateTime()

            if self.simControl.currentTime > self.endConditions.endTime:
                endReached = True
                print("Simulation terminated. Reached end time.")
                break

            #print sim status to console every 50 time steps.
            if int( self.simControl.currentTime * (1 / self.simControl.timeStep)) % 50 == 0:
                print("Current time: %.3f" % self.simControl.currentTime)


            #update the fuel Tank
            m = self.fuelTank.mass - (self.simControl.timeStep * self.parameters.fuelMassFlow)

            if m <= self.endConditions.lowFuelMass:
                endReached = True
                print("Simulation terminated. Ran out of fuel.")
                break

            self.fuelTank.mass = m
            self.fuelTank.volume = self.fuelTank.mass / self.fuelTank.density

            #drain the oxidizer tank
            m = self.oxTank.liquid.RemoveMass(self.parameters.oxMassFlow, self.simControl.timeStep)

            if m <= self.endConditions.lowOxMass:
                endReached = True
                print("Simulation terminated. Ran out of oxidizer.")
                break

            u = self.oxTank.liquid.RemoveEnergy(self.parameters.oxMassFlow, self.simControl.timeStep)
            
            #assuming pressure stays constant (due to active pressure control), update other properties
            self.oxTank.liquid.SetIntrinsicProperties("pressure", self.oxTank.liquid.pressure, "internalEnergy", u)
            self.oxTank.liquid.SetExtrinsicProperties("mass", m)

            self.oxTank.volume = self.oxTank.initialVolume + (self.fuelTank.initialVolume - self.fuelTank.volume)
            
            #find volume of gas phase in NOS tank from expulsion of NOS, fuel
            VN2 = self.oxTank.volume - self.oxTank.liquid.volume

            #find the temperature, enthalpy of the nitrogen added to the NOS tank.
            T = self.pressTank.gas.IsentropicPressureChange(self.oxTank.liquid.pressure)
            hIn = cp.PropsSI('H', 'T', T, 'P', self.oxTank.liquid.pressure, self.pressTank.gas.fluid)

            #numerically solve for flow rate
            def FlowRate():
                a = 0
                b = 5
                c = (a + b) / 2

                def PN2(massFlow):
                    m = self.oxTank.gas.AddMass(massFlow, self.simControl.timeStep)
                    u = self.oxTank.gas.AddEnergy(massFlow, self.simControl.timeStep, hIn)
                    density = m / VN2
                    p = cp.PropsSI('P', 'D', density, 'U', u, self.oxTank.gas.fluid)
                    return p - self.oxTank.liquid.pressure

                while True:
                    fa = PN2(a)
                    fc = PN2(c)

                    if fa * fc < 0:
                        b = c

                    else:
                        a = c 

                    c = (a + b) / 2

                    if abs (PN2(c)) < 2:
                        break

                return c 

            pressurantMassFlow = FlowRate()
            self.pressTank.pressurantMassFlowRate = pressurantMassFlow
            self.pressTank.pressurantMassFlowRateFuel = self.parameters.fuelMassFlow / self.fuelTank.density * self.pressTank.gas.density
            self.pressTank.pressurantMassFlowRateOx = self.pressTank.pressurantMassFlowRate - self.pressTank.pressurantMassFlowRateFuel

            #add pressurant to propellant tank
            m = self.oxTank.gas.AddMass(pressurantMassFlow, self.simControl.timeStep)
            u = self.oxTank.gas.AddEnergy(pressurantMassFlow, self.simControl.timeStep, hIn)
            density = m / VN2
            self.oxTank.gas.SetIntrinsicProperties("density", density, "internalEnergy", u)
            self.oxTank.gas.SetExtrinsicProperties("volume", VN2)

            #remove pressurant from pressurant tank
            m = self.pressTank.gas.RemoveMass(pressurantMassFlow, self.simControl.timeStep)

            if m <= self.endConditions.lowPressurantMass:
                endReached = True
                print("Simulation terminated. Ran out of pressurant.")
                break

            #u = self.pressTank.gas.RemoveEnergy(pressurantMassFlow, self.simControl.timeStep)
            density = m / self.pressTank.volume
            #using a fixed temperature lapse rate to limit the degree of cooling to a reasonable value
            self.pressTank.gas.SetIntrinsicProperties("density", density, "temperature", self.pressTank.gas.temperature - (40/3 * self.simControl.timeStep))
            self.pressTank.gas.SetExtrinsicProperties("volume", self.pressTank.gas.volume)

            #update the log
            self.Log()

        self.log.to_csv("log.csv")