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

        #Option 1 initialize using mass, temperature, and pressure (used for NOS liquid)
        try:
            self.mass = convertToSI(dic["mass"], dic["massUnit"], "mass")
            self.temperature = convertToSI(dic["temperature"], dic["temperatureUnit"], "temperature")
            self.pressure = convertToSI(dic["pressure"], dic["pressureUnit"], "pressure")

            self.density = cp.PropsSI('D', 'P', self.pressure, 'T', self.temperature, self.fluid)
            self.volume = self.mass / self.density
            self.enthalpy = cp.PropsSI('H', 'P', self.pressure, 'T', self.temperature, self.fluid)
            self.internalEnergy = cp.PropsSI('U', 'P', self.pressure, 'T', self.temperature, self.fluid)
            self.sonicVelocity = cp.PropsSI('A', 'P', self.pressure, 'T', self.temperature, self.fluid)
            self.dynamicViscosity = cp.PropsSI('V', 'P', self.pressure, 'T', self.temperature, self.fluid)

        except:
            #Option 2 initialize using volume, pressure, temperature
            try: 
                self.temperature = convertToSI(dic["temperature"], dic["temperatureUnit"], "temperature")
                self.pressure = convertToSI(dic["pressure"], dic["pressureUnit"], "pressure")
                self.volume = convertToSI(dic["volume"], dic["volumeUnit"], "volume")

                self.density = cp.PropsSI('D', 'P', self.pressure, 'T', self.temperature, self.fluid)
                self.mass = self.density * self.volume
                self.enthalpy = cp.PropsSI('H', 'P', self.pressure, 'T', self.temperature, self.fluid)
                self.internalEnergy = cp.PropsSI('U', 'P', self.pressure, 'T', self.temperature, self.fluid)
                self.sonicVelocity = cp.PropsSI('A', 'P', self.pressure, 'T', self.temperature, self.fluid)
                self.dynamicViscosity = cp.PropsSI('V', 'P', self.pressure, 'T', self.temperature, self.fluid)

            except: 
                pass

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