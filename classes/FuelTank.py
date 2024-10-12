from functions.units import *
from classes.State import *

class FuelTank:
    #constants
    name = "" #name of the tank
    volume = 0 #total volume of rigid tank, in m3

    #variables
    liquid = "" #state object of the liquid phase in the tank
    fuelMassFlowRate = 0 #flowrate of fuel
    fuelVolumeFlowRate = 0 #volumerate of fuel
    fuelDensity = 0
    mass = 0
    OFRatio = 0

    def __init__(self):
        pass

    def Load(self, dic):
        self.volume = convertToSI(dic["volume"], dic["volumeUnit"], "volume")
        
        # if self.liquid.fluid == "B100":
        #     self.liqui.fluid = "MethylStearate"
        # if self.liquid.fluid == "RP-1" or self.liquid.fluid == "RP1":
        #     self.liqui.fluid = "n-Decane"
        
        self.liquid = State()
        self.liquid.Load(dic["liquid"])
        
        self.liquid.SetExtrinsicProperties("mass", self.liquid.mass)
        
        self.name = dic["name"]

    def InitLog(self, log, name):
        name += "." + self.name
        log[name + ".fuelMassFlowRate"] = pd.Series(dtype='float64')
        self.liquid.InitLog(log, name)

    def Log(self, log, name):
        name += "." + self.name
        log[name +".fuelMassFlowRate"].iat[-1] = self.fuelMassFlowRate
        self.liquid.Log(log, name)

    def CalcLiquidMassFlow(self, oxMassFlowRate, OF, liquidOx):
        oxVolumeFlow = oxMassFlowRate / liquidOx.density
        self.OFRatio = OF
        self.fuelVolumeFlow = oxVolumeFlow / self.OFRatio        
        self.fuelDensity = cp.PropsSI('D', 'P', self.liquid.pressure, 'T', self.liquid.temperature, self.liquid.fluid)
        self.fuelMassFlowRate = self.fuelDensity * self.fuelVolumeFlow
        return self.fuelMassFlowRate