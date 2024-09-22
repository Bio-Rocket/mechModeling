from functions.units import *
from classes.State import *

class PressurantTank:
    #constants
    name = "" #name of the tank
    volume = 0 #total volume of rigid tank, in m3

    #variables
    gas = "" #state object of the gas phase in the tank

    def __init__(self):
        pass

    def Load(self, dic):
        self.volume = convertToSI(dic["volume"], dic["volumeUnit"], "volume")
        self.gas = State()
        self.gas.Load(dic["gas"])
        self.name = dic["name"]

    def InitLog(self, log, name):
        name += "." + self.name
        self.gas.InitLog(log, name)

    def Log(self, log, name):
        name += "." + self.name
        self.gas.Log(log, name)

    def RemovegasMass(self, massFlowRate, timeStep):
        self.gas.mass -= massFlowRate * timeStep

        self.RemovegasEnergy(massFlowRate, timeStep)

    def RemovegasEnergy(self, massFlowRate, timeStep):
        #assuming no heat transfer or work done, no mass in, negligible changes in K.E., P.E. 
        #applying conservation of energy gives:
        #deltaM*h_out +m2*u2 - m1*u1 = 0
        m2 = self.gas.mass
        m1 = m2 + massFlowRate * timeStep
        deltaM = m1 - m2
        hOut = cp.PropsSI('H', 'P', self.gas.pressure, 'T', self.gas.temperature, self.gas.fluid)
        u1 = self.gas.internalEnergy

        u2 = (m1 * u1 - deltaM * hOut) / m2

        #assuming pressure stays constant (due to active pressure control), update other properties
        self.gas.internalEnergy = u2
        self.gas.temperature = cp.PropsSI('T', 'P', self.gas.pressure, 'U', u2, self.gas.fluid)
        self.gas.density = cp.PropsSI('D', 'P', self.gas.pressure, 'U', u2, self.gas.fluid)
        self.gas.volume = self.gas.mass / self.gas.density
        self.gas.enthalpy = cp.PropsSI('H', 'P', self.gas.pressure, 'U', u2, self.gas.fluid)
