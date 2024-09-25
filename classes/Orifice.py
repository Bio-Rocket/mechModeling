from functions.units import *
from classes.State import *
import math

class Orifice:
    #constant
    name = "" #The name of the instance of class Orifice.
    diameter = 0 #The diameter of the orifice, in m.
    area = 0 #The cross-sectional area of the orifice, in m^2.

    #variable
    pressureRatio = 0 #The ratio of the reservoir pressure to the back pressure, dimensionless.
    choked = True #Whether or not the orifice is choked based on the pressure ratio
    massFlowRate = 0 #The mass flow rate through the orifice based on the upstream and downstream conditions, in kg/s

    inlet = "" #An instance of class state representing the fluid at the inlet.
    outlet = "" #An instance of class state representing the fluid at the outlet.

    def __init__(self):
        pass

    def Load(self, dic):
        self.name = dic["name"]
        self.diameter = convertToSI(dic["diameter"], dic["diameterUnit"], "length")
        self.area = math.pi * self.diameter ** 2 / 4

    def InitLog(self, log, name):
        name += "." + self.name
        log[name + ".pressureRatio"] = pd.Series(dtype='float64')
        log[name + ".choked"] = pd.Series(dtype='str')
        log[name + ".massFlowRate"] = pd.Series(dtype='str')
        
    def Log(self, log, name):
        name += "." + self.name
        log[name +".pressureRatio"].iat[-1] = self.pressureRatio
        log[name +".choked"].iat[-1] = str(self.choked)
        log[name +".massFlowRate"].iat[-1] = str(self.massFlowRate)

    def CalcMassFlow(self):
        gamma = cp.PropsSI('Cpmass', 'P', self.inlet.pressure, 'T', self.inlet.temperature, self.inlet.fluid) / cp.PropsSI('Cvmass', 'P', self.inlet.pressure, 'T', self.inlet.temperature, self.inlet.fluid)
        R = cp.PropsSI('GAS_CONSTANT', self.inlet.fluid) / cp.PropsSI('MOLAR_MASS', self.inlet.fluid)

        self.pressureRatio = self.inlet.pressure / self.outlet.pressure
        gammaTerm = ((gamma + 1) / 2) ** (gamma / (gamma - 1))

        if self.pressureRatio > gammaTerm:
            self.choked = True
            gammaTerm = math.sqrt(gamma)*( ((gamma + 1)/2) ** (-(gamma + 1) /(2 * (gamma - 1))))

            self.massFlowRate = (self.inlet.pressure * self.area / math.sqrt(R * self.inlet.temperature)) * gammaTerm
        else:
            self.choked = False

    