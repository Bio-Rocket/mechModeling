from functions.units import *
from classes.State import *
import math

class FlowLine:
    #constants
    innerDiameter = 0 #The inner diameter of the flow line, in m.
    length = 0 #The length of the flow line, in m.
    area = 0 #The cross sectional area, in m^2.
    name = "" #Name of the flow line.

    #variables
    velocity = 0 #The bulk velocity of the fluid in the line, in m/s.
    machNumber = 0 #The mach number of the fluid in the line, dimensionless.
    reynoldsNumber = 0 #The Reynold's number of the fluid in the line, dimensionless.
    pressureDrop = 0 #The pressure drop across the flow line, in Pa.

    inlet = "" #An instance of class State representing the inlet of the flow line.
    outlet = "" #An instance of class State representing the outlet of the flow line.

    def __init__(self):
        pass

    def Load(self, dic):
        self.name = dic["name"]
        self.length = convertToSI(dic["length"], dic["lengthUnit"], "length")
        self.innerDiameter = convertToSI(dic["innerDiameter"], dic["innerDiameterUnit"], "length")
        self.area = math.pi * self.innerDiameter ** 2 / 4

    def InitLog(self, log, name):
        name += "." + self.name
        log[name + ".velocity"] = pd.Series(dtype='float64')
        log[name + ".machNumber"] = pd.Series(dtype='float64')
        log[name + ".reynoldsNumber"] = pd.Series(dtype='float64')

    def Log(self, log, name):
        name += "." + self.name
        log[name +".velocity"].iat[-1] = self.velocity
        log[name +".machNumber"].iat[-1] = self.machNumber
        log[name +".reynoldsNumber"].iat[-1] = self.reynoldsNumber

    def UpdateFlowLine(self, massFlowRate):
        self.machNumber = self.velocity / self.inlet.sonicVelocity
        self.velocity = massFlowRate / (self.inlet.density * self.area)
        self.reynoldsNumber = self.inlet.density * self.velocity * self.innerDiameter / self.inlet.dynamicViscosity