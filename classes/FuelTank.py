from functions.units import *
from classes.State import *

class FuelTank:
    #constants
    name = "" #name of the tank
    initialVolume = 0 #the initial volume of the tank, in m^3
    volume = 0 #total volume of tank, in m3
    mass = 0 #the mass of the fluid in the tank, in m3
    density = 0 #density, in kg/m^3

    def __init__(self):
        pass

    def Load(self, dic):
        self.volume = convertToSI(dic["volume"], dic["volumeUnit"], "volume")
        self.initialVolume = self.volume
        self.mass = convertToSI(dic["mass"], dic["massUnit"], "mass")
        self.name = dic["name"]
        self.density = self.mass / self.volume

    def InitLog(self, log, name):
        name += "." + self.name
        log[name + ".mass"] = pd.Series(dtype='float64')
        log[name + ".volume"] = pd.Series(dtype='float64')

    def Log(self, log, name):
        name += "." + self.name
        log[name +".mass"].iat[-1] = self.mass
        log[name +".volume"].iat[-1] = self.volume
