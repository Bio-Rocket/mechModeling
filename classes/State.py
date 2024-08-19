from functions.units import *

import pandas as pd

class State:
    name = "" #the name given to the state

    #variables
    #extrinsic properties
    mass = 0 #the mass of the phase, in kg

    #intrinsic properties

    def __init__(self):
        pass

    def Load(self, dic):
        self.mass = convertToSI(dic["mass"], dic["massUnit"], "mass")
        self.name = dic["name"]

    def InitLog(self, log, name):
        name += "." + self.name
        log[name + ".mass"] = pd.Series(dtype='float64')

    def Log(self, log, name):
        name += "." + self.name
        log[name +".mass"].iat[-1] = self.mass