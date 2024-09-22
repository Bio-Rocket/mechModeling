from functions.units import *
from classes.State import *

class OxTank:
    #constants
    name = "" #name of the tank
    volume = 0 #total volume of rigid tank, in m3

    #variables
    liquid = "" #state object of the liquid phase in the tank

    def __init__(self):
        pass

    def Load(self, dic):
        self.volume = convertToSI(dic["volume"], dic["volumeUnit"], "volume")
        self.liquid = State()
        self.liquid.Load(dic["liquid"])
        self.name = dic["name"]

    def InitLog(self, log, name):
        name += "." + self.name
        self.liquid.InitLog(log, name)

    def Log(self, log, name):
        name += "." + self.name
        self.liquid.Log(log, name)

    def RemoveLiquidMass(self, massFlowRate, timeStep):
        self.liquid.mass -= massFlowRate * timeStep

        self.RemoveLiquidEnergy(massFlowRate, timeStep)

    def RemoveLiquidEnergy(self, massFlowRate, timeStep):
        #assuming no heat transfer or work done, no mass in, negligible changes in K.E., P.E. 
        #applying conservation of energy gives:
        #deltaM*h_out +m2*u2 - m1*u1 = 0
        m2 = self.liquid.mass
        m1 = m2 + massFlowRate * timeStep
        deltaM = m1 - m2
        hOut = cp.PropsSI('H', 'P', self.liquid.pressure, 'T', self.liquid.temperature, self.liquid.fluid)
        u1 = self.liquid.internalEnergy

        u2 = (m1 * u1 - deltaM * hOut) / m2
        
        #if flow rate is large, enthalpy calculated here sometimes becomes negative
        #from which exit calculation and return values
        if u2 <= 0:
            return
        
        #assuming pressure stays constant (due to active pressure control), update other properties
        self.liquid.internalEnergy = u2
        self.liquid.temperature = cp.PropsSI('T', 'P', self.liquid.pressure, 'U', u2, self.liquid.fluid)
        self.liquid.density = cp.PropsSI('D', 'P', self.liquid.pressure, 'U', u2, self.liquid.fluid)
        self.liquid.volume = self.liquid.mass / self.liquid.density
        self.liquid.enthalpy = cp.PropsSI('H', 'P', self.liquid.pressure, 'U', u2, self.liquid.fluid)
