from functions.units import *
from classes.State import *

class OxTank:
    #constants
    name = "" #name of the tank
    volume = 0 #total volume of rigid tank, in m3
    initialVolume = 0 #the total volume of the tank, initial.

    #variables
    liquid = "" #state object of the liquid phase in the tank
    gas = "" #State object of the pressurant phase in the tank

    def __init__(self):
        pass

    def Load(self, dic):
        self.volume = convertToSI(dic["volume"], dic["volumeUnit"], "volume")
        self.initialVolume = self.volume

        self.liquid = State()
        self.liquid.Load(dic["liquid"])

        self.gas = State()
        self.gas.Load(dic["gas"])

        self.gas.SetExtrinsicProperties("volume", self.volume - self.liquid.volume)

        self.name = dic["name"]

    def InitLog(self, log, name):
        name += "." + self.name
        self.liquid.InitLog(log, name)
        self.gas.InitLog(log, name)

    def Log(self, log, name):
        name += "." + self.name
        self.liquid.Log(log, name)
        self.gas.Log(log, name)
