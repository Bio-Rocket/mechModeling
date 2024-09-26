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

        T01 = 288.15
        P01 = 39989592.300560005
        rho01 = 374.3882243409955

        if self.pressureRatio > gammaTerm:
            self.choked = True
            self.massFlowRate = ((rho01/(P01 ** (1/gamma)))* ((2/(gamma + 1)) ** (1/(gamma - 1))))*self.area*(math.sqrt(((2 * gamma)*(P01 ** (1/ gamma)))/((gamma + 1) * rho01)))*(self.inlet.pressure ** ((gamma + 1)/(2* gamma)))
            #equation 3.33 of Theo & Keith
            
        else:
            self.choked = False
            self.massFlowRate = (rho01 * ((self.outlet.pressure / P01) ** (1 / gamma))) * self.area * math.sqrt(((2 * gamma) / (gamma - 1)) * (self.inlet.pressure / (rho01 * ((self.inlet.pressure / P01) ** (1 / gamma)))) * (1 - ((self.outlet.pressure / self.inlet.pressure) ** ((gamma - 1) / (gamma)))))
            #equation 3.42 of Theo & Keith
            

    