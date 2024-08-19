from functions.units import *
from classes.State import *

class Tank:
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