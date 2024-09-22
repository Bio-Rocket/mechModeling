from functions.units import *

class Parameters:
    oxMassFlow = 0 #oxidizer mass flow rate, in kg/s

    def __init__(self):
        pass

    def load(self, dic, tank):
        if tank == "ox":
            self.oxMassFlow = convertToSI(dic["oxMassFlow"], dic["oxMassFlowUnit"], "mass")
        elif tank == "pressurant":
            self.pressurantMassFlow = convertToSI(dic["pressurantMassFlow"], dic["pressurantMassFlowUnit"], "mass")
