from functions.units import *
from classes.State import *

class PressTank:
    #constants
    name = "" #name of the tank
    volume = 0 #total volume of rigid tank, in m3

    #variables
    gas = "" #state object of the liquid phase in the tank
    pressurantMassFlowRate = ""

    def __init__(self):
        pass

    def Load(self, dic):
        self.volume = convertToSI(dic["volume"], dic["volumeUnit"], "volume")
        self.gas = State()
        self.gas.Load(dic["gas"])
        self.name = dic["name"]

    def InitLog(self, log, name):
        name += "." + self.name
        log[name + ".pressurantMassFlowRate"] = pd.Series(dtype='float64')
        self.gas.InitLog(log, name)

    def Log(self, log, name):
        name += "." + self.name
        log[name +".pressurantMassFlowRate"].iat[-1] = self.pressurantMassFlowRate
        self.gas.Log(log, name)

    def CalcGassMassFlow(self, oxMassFlowRate, liquidOx):
        oxVolumeFlow = oxMassFlowRate / liquidOx.density
        pressurantDensity = cp.PropsSI('D', 'P', liquidOx.pressure, 'T', liquidOx.temperature, self.gas.fluid)
        self.pressurantMassFlowRate = pressurantDensity * oxVolumeFlow

    def RemoveGasMass(self, oxMassFlowRate, timeStep, liquidOx):
        self.CalcGassMassFlow(oxMassFlowRate, liquidOx)
        self.gas.mass -= self.pressurantMassFlowRate * timeStep

        self.RemoveGasEnergy(timeStep)

    def RemoveGasEnergy(self, timeStep):
        #assuming no heat transfer or work done, no mass in, negligible changes in K.E., P.E. 
        #applying conservation of energy gives:
        #deltaM*h_out +m2*u2 - m1*u1 = 0
        m2 = self.gas.mass
        m1 = m2 + self.pressurantMassFlowRate * timeStep
        deltaM = m1 - m2
        hOut = cp.PropsSI('H', 'P', self.gas.pressure, 'T', self.gas.temperature, self.gas.fluid)
        u1 = self.gas.internalEnergy

        u2 = (m1 * u1 - deltaM * hOut) / m2

        #using constant volume, new mass, and new internal energy, find other properties
        self.gas.density = self.gas.mass / self.gas.volume
        self.gas.internalEnergy = u2
        self.gas.temperature = cp.PropsSI('T', 'D', self.gas.density, 'U', self.gas.internalEnergy, self.gas.fluid)
        self.gas.enthalpy = cp.PropsSI('H', 'D', self.gas.density, 'U', self.gas.internalEnergy, self.gas.fluid)
        self.gas.pressure = cp.PropsSI('P', 'D', self.gas.density, 'U', self.gas.internalEnergy, self.gas.fluid)