from functions.units import *
from classes.State import *

class PressTank:
    #constants
    name = "" #name of the tank
    volume = 0 #total volume of rigid tank, in m3

    #variables
    gas = "" #state object of the gas phase in the tank
    initial = "" #state object representing the initial state of the tank.
    pressurantMassFlowRate = ""

    def __init__(self):
        pass

    def Load(self, dic):
        self.volume = convertToSI(dic["volume"], dic["volumeUnit"], "volume")

        self.gas = State()
        self.gas.Load(dic["gas"])

        self.initial = State()
        self.initial.Load(dic["gas"])

        self.name = dic["name"]

    def InitLog(self, log, name):
        name += "." + self.name
        log[name + ".pressurantMassFlowRate"] = pd.Series(dtype='float64')
        self.gas.InitLog(log, name)

    def Log(self, log, name):
        name += "." + self.name
        log[name +".pressurantMassFlowRate"].iat[-1] = self.pressurantMassFlowRate
        self.gas.Log(log, name)

    #calculates gas mass flow rate required to keep ullage pressure in oxTank constant
    def CalcGassMassFlow(self, oxMassFlowRate, liquidOx):
        oxVolumeFlow = oxMassFlowRate / liquidOx.density
        pressurantDensity = cp.PropsSI('D', 'P', liquidOx.pressure, 'T', liquidOx.temperature, self.gas.fluid)
        self.pressurantMassFlowRate = pressurantDensity * oxVolumeFlow