from functions.units import *

class Parameters:
    oxMassFlow = 0 #oxidizer mass flow rate, in kg/s

    def __init__(self):
        pass

    def load(self, dic):
        self.oxMassFlow = convertToSI(dic["oxMassFlow"], dic["oxMassFlowUnit"], "mass")