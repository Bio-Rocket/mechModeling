from functions.units import *

class State:
    #extrinsic properties
    mass = 0 #the mass of the phase, in kg

    #intrinsic properties

    def __init__(self):
        pass

    def load(self, dic):
        self.mass = convertToSI(dic["mass"], dic["massUnit"], "mass")