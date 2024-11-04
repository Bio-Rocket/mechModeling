from functions.units import *
import CoolProp.CoolProp as cp

import pandas as pd

class State:
    #constant
    name = "" #the name given to the state
    fluid = "" #the coolprop name of the fluid
    R = 0 #Specific gas constant, in J/kg*K

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
    entropy = 0 #entropy of the phase, in J/kg*K
    dynamicViscosity = 0 #dynamic viscosity, in Pa * s

    def __init__(self):
        pass

    def Load(self, dic):
        
        self.name = dic["name"]
        self.fluid = dic["fluid"]
        self.R = cp.PropsSI('GAS_CONSTANT', self.fluid)/cp.PropsSI('MOLAR_MASS', self.fluid)

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
        log[name + ".entropy"] = pd.Series(dtype='float64')

    def Log(self, log, name):
        name += "." + self.name
        log[name +".mass"].iat[-1] = self.mass
        log[name + ".density"].iat[-1] = self.density
        log[name + ".temperature"].iat[-1] = self.temperature
        log[name + ".pressure"].iat[-1] = self.pressure
        log[name + ".enthalpy"].iat[-1] = self.enthalpy
        log[name + ".internalEnergy"].iat[-1] = self.internalEnergy
        log[name + ".volume"].iat[-1] = self.volume
        log[name + ".entropy"].iat[-1] = self.entropy

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
            self.entropy = cp.PropsSI('S', 'P', self.pressure, 'T', self.temperature, self.fluid)

            #CoolProp does not have a model for dynamic viscosity of nitrous.
            try:
                self.dynamicViscosity = cp.PropsSI('V', 'P', self.pressure, 'T', self.temperature, self.fluid)

            except:
                pass

        #Option 2: Set intrinsic property values using enthalpy and density
        elif prop1 == "enthalpy" and prop2 == "density":
            self.enthalpy = value1
            self.density = value2

            self.temperature = cp.PropsSI('T', 'H', self.enthalpy, 'D', self.density, self.fluid)
            self.pressure = cp.PropsSI('P', 'H', self.enthalpy, 'D', self.density, self.fluid)
            self.internalEnergy = cp.PropsSI('U', 'H', self.enthalpy, 'D', self.density, self.fluid)
            self.sonicVelocity = cp.PropsSI('A', 'H', self.enthalpy, 'D', self.density, self.fluid)
            self.entropy = cp.PropsSI('S', 'H', self.enthalpy, 'D', self.density, self.fluid)

            #CoolProp does not have a model for dynamic viscosity of nitrous.
            try:
                self.dynamicViscosity = cp.PropsSI('V', 'H', self.enthalpy, 'D', self.density, self.fluid)

            except:
                pass

        #Option 3: Set intrinsic property values using density and pressure
        elif prop1 == "density" and prop2 == "pressure":
            self.density = value1
            self.pressure = value2

            self.temperature = cp.PropsSI('T', 'D', self.density, 'P', self.pressure, self.fluid)
            self.enthalpy = cp.PropsSI('H', 'D', self.density, 'P', self.pressure, self.fluid)
            self.internalEnergy = cp.PropsSI('U', 'D', self.density, 'P', self.pressure, self.fluid)
            self.sonicVelocity = cp.PropsSI('A', 'D', self.density, 'P', self.pressure, self.fluid)
            self.entropy = cp.PropsSI('S', 'D', self.density, 'P', self.pressure, self.fluid)

            #CoolProp does not have a model for dynamic viscosity of nitrous.
            try:
                self.dynamicViscosity = cp.PropsSI('V', 'D', self.density, 'P', self.pressure, self.fluid)

            except:
                pass

        #Option 4: Set intrinsic property values using pressure and internal energy
        elif prop1 == "pressure" and prop2 == "internalEnergy":
            self.pressure = value1
            self.internalEnergy = value2

            self.temperature = cp.PropsSI('T', 'P', self.pressure, 'U', self.internalEnergy, self.fluid)
            self.density = cp.PropsSI('D', 'P', self.pressure, 'U', self.internalEnergy, self.fluid)
            self.enthalpy = cp.PropsSI('H', 'P', self.pressure, 'U', self.internalEnergy, self.fluid)
            self.sonicVelocity = cp.PropsSI('A', 'P', self.pressure, 'U', self.internalEnergy, self.fluid)
            self.entropy = cp.PropsSI('S', 'P', self.pressure, 'U', self.internalEnergy, self.fluid)
            
            #CoolProp does not have a model for dynamic viscosity of nitrous.
            try:
                self.dynamicViscosity = cp.PropsSI('V', 'P', self.pressure, 'U', self.internalEnergy, self.fluid)

            except:
                pass

        #Option 5: Set intrinsic property values using density and internal energy
        elif prop1 == "density" and prop2 == "internalEnergy":
            self.density = value1
            self.internalEnergy = value2

            self.temperature = cp.PropsSI('T', 'D', self.density, 'U', self.internalEnergy, self.fluid)
            self.enthalpy = cp.PropsSI('H', 'D', self.density, 'U', self.internalEnergy, self.fluid)
            self.pressure = cp.PropsSI('P', 'D', self.density, 'U', self.internalEnergy, self.fluid)
            self.sonicVelocity = cp.PropsSI('A', 'D', self.density, 'U', self.internalEnergy, self.fluid)
            self.entropy = cp.PropsSI('S', 'D', self.density, 'U', self.internalEnergy, self.fluid)

            #CoolProp does not have a model for dynamic viscosity of nitrous.
            try:
                self.dynamicViscosity = cp.PropsSI('V', 'D', self.density, 'U', self.internalEnergy, self.fluid)

            except:
                pass

        #Option 6: Set intrinsic property values using internal energy and entropy
        #note, as of V 6.6, coolprop does not yet support this pair of inputs.
        elif prop1 == "internalEnergy" and prop2 == "entropy":
            self.internalEnergy = value1
            self.entropy = value2

            self.temperature = cp.PropsSI('T', 'U', self.internalEnergy, 'S', self.entropy, self.fluid)
            self.enthalpy = cp.PropsSI('H', 'U', self.internalEnergy, 'S', self.entropy, self.fluid)
            self.pressure = cp.PropsSI('P', 'U', self.internalEnergy, 'S', self.entropy, self.fluid)
            self.sonicVelocity = cp.PropsSI('A', 'U', self.internalEnergy, 'S', self.entropy, self.fluid)
            self.density = cp.PropsSI('D', 'U', self.internalEnergy, 'S', self.entropy, self.fluid)

            try:
                self.dynamicViscosity = cp.PropsSI('V', 'U', self.internalEnergy, 'S', self.entropy, self.fluid)

            except:
                pass

        elif prop1 == "density" and prop2 == "temperature":
            self.density = value1
            self.temperature = value2

            self.internalEnergy = cp.PropsSI('U', 'D', self.density, 'T', self.temperature, self.fluid)
            self.entropy = cp.PropsSI('S', 'D', self.density, 'T', self.temperature, self.fluid)
            self.enthalpy = cp.PropsSI('H', 'D', self.density, 'T', self.temperature, self.fluid)
            self.pressure = cp.PropsSI('P', 'D', self.density, 'T', self.temperature, self.fluid)
            self.sonicVelocity = cp.PropsSI('A', 'D', self.density, 'T', self.temperature, self.fluid)
            
            try:
                self.dynamicViscosity = cp.PropsSI('V', 'D', self.density, 'T', self.temperature, self.fluid)

            except:
                pass

    def RemoveMass(self, massFlowRate, timeStep):
        m = self.mass - massFlowRate * timeStep
        return m

    def RemoveEnergy(self, massFlowRate, timeStep):
        #assuming no heat transfer or work done, no mass in, negligible changes in K.E., P.E. 
        #applying conservation of energy gives:
        #deltaM*h_out +m2*u2 - m1*u1 = 0
        m2 = self.mass
        m1 = m2 + massFlowRate * timeStep
        deltaM = m1 - m2

        u2 = (m1 * self.internalEnergy - deltaM * self.enthalpy) / m2
        return u2

    def AddMass(self, massFlowRate, timeStep):
        return self.mass + massFlowRate * timeStep

    #requires inlet enthalpy, if undefined, assume equal to enthalpy of this state
    def AddEnergy(self, massFlowRate, timeStep, hIn=enthalpy):
        m2 = self.mass
        m1 = m2 - massFlowRate * timeStep
        deltaM = m2 - m1
        u1 = self.internalEnergy

        u2 = (m1 * u1 + deltaM * hIn) / m2
        return u2

    def RemoveEntropy(self, massFlowRate, timeStep):
        #assuming no heat transfer, reversible process
        #applying entropy balance gives:
        #m2 * s2 - m1 * s1 = deltaM * sOut
        m2 = self.mass
        m1 = m2 + massFlowRate * timeStep
        deltaM = m1 - m2

        s2 = (deltaM * self.entropy + m1 * self.entropy) / m2
        return s2

    def IsentropicVolumeChange(self, V2):
        V1 = self.volume
        P1 = self.pressure
        T1 = self.temperature
        gamma = cp.PropsSI('Cpmass', 'P', self.pressure, 'T', self.temperature, self.fluid) / cp.PropsSI('Cvmass', 'P', self.pressure, 'T', self.temperature, self.fluid)
        P2 = P1 * ((V1 / V2) ** gamma)
        T2 = T1 * ( (P2 / P1) ** ((gamma - 1) / gamma))
        return P2, T2

    def IsentropicPressureChange(self, P2):
        P1 = self.pressure
        T1 = self.temperature
        gamma = cp.PropsSI('Cpmass', 'P', self.pressure, 'T', self.temperature, self.fluid) / cp.PropsSI('Cvmass', 'P', self.pressure, 'T', self.temperature, self.fluid)
        T2 = T1 * ( (P2 / P1) ** ((gamma - 1) / gamma))
        return T2