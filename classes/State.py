from functions.units import *
import CoolProp.CoolProp as cp

import pandas as pd

class State:
    #constant
    name = "" #the name given to the state
    fluid = "" #the coolprop name of the fluid

    #variables
    #extrinsic properties
    mass = 0 #the mass of the phase, in kg
    volume = 0 #volume occupied by the phase, in m^3

    #intrinsic properties
    density = 0 #density of the phase, in kg/m^3
    temperature = 0 #temperature of the phase, in K
    pressure = 0 #pressure of the phase, in Pa
    enthalpy = 0 #enthalpy of the phase, in J/kg
    internalEnergy = 0 #internal energy of the phase, in J/kg
    sonicVelocity = 0 #speed of sound, in m/s
    dynamicViscosity = 0 #dynamic viscosity, in Pa * s

    def __init__(self):
        pass

    def Load(self, dic):
        
        self.name = dic["name"]
        self.fluid = dic["fluid"]

        #can initialise intrinsic properties using any two properties. 

        #Option 1: using temperature, and pressure
        if "pressure" in dic and "temperature" in dic:
            self.SetIntrinsicProperties("temperature", convertToSI(dic["temperature"], dic["temperatureUnit"], "temperature"), "pressure", convertToSI(dic["pressure"], dic["pressureUnit"], "pressure"))



        #No other options currently implemented, but they could be.

        #Can instantiate extrinsic properties using any single property

        #Option 1: Using mass.
        if "mass" in dic:
            self.SetExtrinsicProperties("mass", convertToSI(dic["mass"], dic["massUnit"], "mass"))
        
        #Option 2: Using volume.
        elif "volume" in dic:
            self.SetExtrinsicProperties("volume", convertToSI(dic["volume"], dic["volumeUnit"], "volume"))
                    
    def InitLog(self, log, name):
        name += "." + self.name
        log[name + ".mass"] = pd.Series(dtype='float64')
        log[name + ".density"] = pd.Series(dtype='float64')
        log[name + ".temperature"] = pd.Series(dtype='float64')
        log[name + ".pressure"] = pd.Series(dtype='float64')
        log[name + ".enthalpy"] = pd.Series(dtype='float64')
        log[name + ".internalEnergy"] = pd.Series(dtype='float64')
        log[name + ".volume"] = pd.Series(dtype='float64')

    def Log(self, log, name):
        name += "." + self.name
        log[name +".mass"].iat[-1] = self.mass
        log[name + ".density"].iat[-1] = self.density
        log[name + ".temperature"].iat[-1] = self.temperature
        log[name + ".pressure"].iat[-1] = self.pressure
        log[name + ".enthalpy"].iat[-1] = self.enthalpy
        log[name + ".internalEnergy"].iat[-1] = self.internalEnergy
        log[name + ".volume"].iat[-1] = self.volume

    def SetExtrinsicProperties(self, prop, value):

        #Option 1: Set extrinsic property values using volume
        if prop == "volume":
            self.volume = value
            self.mass = self.volume * self.density

        #Option 2: Set extrinsic property values using mass
        elif prop == "mass":
            self.mass = value
            self.volume = self.mass / self.density

        else:
            raise ValueError("Setting extrinsic properties using %s is not supported." % prop)

    def SetIntrinsicProperties(self, prop1, value1, prop2, value2):

        #Option 1: Set intrinsic property values using temperature and pressure
        if prop1 == "temperature" and prop2 == "pressure":
            self.temperature = value1
            self.pressure = value2

            self.density = cp.PropsSI('D', 'P', self.pressure, 'T', self.temperature, self.fluid)
            self.enthalpy = cp.PropsSI('H', 'P', self.pressure, 'T', self.temperature, self.fluid)
            self.internalEnergy = cp.PropsSI('U', 'P', self.pressure, 'T', self.temperature, self.fluid)
            self.sonicVelocity = cp.PropsSI('A', 'P', self.pressure, 'T', self.temperature, self.fluid)

            #CoolProp does not have a model for dynamic viscosity of nitrous.
            try:
                self.dynamicViscosity = cp.PropsSI('V', 'P', self.pressure, 'T', self.temperature, self.fluid)

            except:
                pass

        elif prop1 == "pressure" and prop2 == "internalEnergy":
            self.pressure = value1
            self.internalEnergy = value2

            self.temperature = cp.PropsSI('T', 'P', self.pressure, 'U', self.internalEnergy, self.fluid)
            self.density = cp.PropsSI('D', 'P', self.pressure, 'U', self.internalEnergy, self.fluid)
            self.enthalpy = cp.PropsSI('H', 'P', self.pressure, 'U', self.internalEnergy, self.fluid)
            self.sonicVelocity = cp.PropsSI('A', 'P', self.pressure, 'U', self.internalEnergy, self.fluid)
            
            #CoolProp does not have a model for dynamic viscosity of nitrous.
            try:
                self.dynamicViscosity = cp.PropsSI('V', 'P', self.pressure, 'U', self.internalEnergy, self.fluid)

            except:
                pass

        elif prop1 == "density" and prop2 == "internalEnergy":
            self.density = value1
            self.internalEnergy = value2

            self.temperature = cp.PropsSI('T', 'D', self.density, 'U', self.internalEnergy, self.fluid)
            self.enthalpy = cp.PropsSI('H', 'D', self.density, 'U', self.internalEnergy, self.fluid)
            self.pressure = cp.PropsSI('P', 'D', self.density, 'U', self.internalEnergy, self.fluid)
            self.sonicVelocity = cp.PropsSI('A', 'D', self.density, 'U', self.internalEnergy, self.fluid)

            #CoolProp does not have a model for dynamic viscosity of nitrous.
            try:
                self.dynamicViscosity = cp.PropsSI('V', 'D', self.density, 'U', self.internalEnergy, self.fluid)

            except:
                pass

