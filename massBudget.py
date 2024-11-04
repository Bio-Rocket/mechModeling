from functions.units import *
import math
import CoolProp.CoolProp as cp
from rocketcea.cea_obj import CEA_Obj, add_new_fuel, add_new_oxidizer
from rocketcea.units import add_user_units
from matplotlib import pyplot as plt

fuelPVLength = 0
NOSPVLength = 0
N2PVLength = 0

def NOSPVMass(volume):
    density = 2710 #kg/m^3
    ID = convertToSI(5.75, "in", "length")
    A = math.pi * ID ** 2 / 4
    NOSPVLength = volume / A 
    OD = convertToSI(6, "in", "length")
    A = math.pi * (OD ** 2 - ID **2) / 4
    return NOSPVLength * A * density, NOSPVLength

def FuelPVMass(volume):
    density = 2710 #kg/m^3
    ID = convertToSI(3.75, "in", "length")
    A = math.pi * ID ** 2 / 4
    fuelPVLength = volume / A 
    OD = convertToSI(4, "in", "length")
    A = math.pi * (OD ** 2 - ID **2) / 4
    return fuelPVLength * A * density, fuelPVLength

def N2PVMass(volume):
    density = 2710 #kg/m^3
    ID = convertToSI(3, "in", "length")
    A = math.pi * ID ** 2 / 4
    N2PVLength = volume / A 
    OD = convertToSI(4, "in", "length")
    A = math.pi * (OD ** 2 - ID **2) / 4
    return N2PVLength * A * density, N2PVLength

def N2AirframeMass(volume):
    ID = convertToSI(3, "in", "length")
    A = math.pi * ID ** 2 / 4
    length = volume / A 
    return 1.537596262 * length

#calculates the amount of volume occupied by the fuel tank in the nitrous tank
def FuelDeadVolume(volume):
    #v0 = 0.000295677444 #dead volume of fuel tank at 0 fuel volume
    #top pv volume = 0.000104
    #fuel wall volume = 0.000170
    #single bolt volume = 0.000001, x 16 = 0.000016
    #lower bulk head = 0.000141"
    #total volume = 0.001367
    v0 = 0.001367

    ID = convertToSI(3.75, "in", "length")
    A = math.pi * ID ** 2 / 4
    length = volume / A 
    OD = convertToSI(4, "in", "length")
    A = math.pi * (OD ** 2 - ID **2) / 4
    wallVolume = A * length

    return volume + v0 + wallVolume

C = CEA_Obj(oxName='N2O', fuelName='ETHANOL')

''' finding optimal expansion ratio
def getEps(C, mr, pc, pa):
    a = 2
    b = 100
    c = (a + b) / 2
    mr = 6.5
    #returns the pressure ratio minus the ambient pressure ratio
    def g(x, C, mr, pc, pa):
        Pr = C.get_PcOvPe(Pc=pc, MR=mr, eps=x)
        PrAmb = pc / pa
        return Pr - PrAmb

    while True:
        #print(a, c, b)
        fa = g(a, C, mr, pc, pa)
        fc = g(c, C, mr, pc, pa)

        if fa * fc < 0:
            b = c

        else:
            a = c

        c = (a + b) /2

        if abs(fc) < 0.001:
            break

    return c

chamberPressure = 809.9529469
exitPressure = 12
expansionRatio = getEps(C, 1, chamberPressure,exitPressure)'''

''' finding optimal OF ratio
OF = []
equilibriumIsp = []
frozenIsp = []
for i in range(4250, 5500):
    OF.append(i/1000)
    equilibriumIsp.append(C.get_Isp(Pc=chamberPressure, MR=i/1000, eps=expansionRatio, frozen=0, frozenAtThroat=0))
    frozenIsp.append(C.get_Isp(Pc=chamberPressure, MR=i/1000, eps=expansionRatio, frozen=1, frozenAtThroat=1))


frozenMax = max(frozenIsp)
frozenMaxIndex = frozenIsp.index(frozenMax)
frozenMaxOF = OF[frozenMaxIndex]

equilibriumMax = max(equilibriumIsp)
equilibriumMaxIndex = equilibriumIsp.index(equilibriumMax)
equilibriumMaxOF = OF[equilibriumMaxIndex]

print(frozenMaxOF, equilibriumMaxOF)
print((frozenMaxOF + equilibriumMaxOF) / 2)'''

''' plotting Isp curves
fig, ax = plt.subplots()

ax.plot(OF, equilibriumIsp)
ax.plot(OF, frozenIsp)
ax.set_ylabel("Specific Impulse (s)")
ax.set_xlabel("O/F Ratio")
ax.legend(["Equilibrium", "Frozen"])
plt.show()
'''

#densities
rhoNOS = cp.PropsSI('D', 'P', convertToSI(1350, "psi", "pressure"), 'T', convertToSI(15, "C", "temperature"), "NITROUSOXIDE")
rhoFuel = cp.PropsSI('D', 'P', convertToSI(1350, "psi", "pressure"), 'T', convertToSI(15, "C", "temperature"), "ETHANOL") #880

TN2start = 288.15
TN2HighEnd = 213.8
TN2LowEnd = 293
PN2HighStart = 5800
PN2HighEnd = 1600
rhoN2HighStart = cp.PropsSI('D', 'P', convertToSI(5800, "psi", "pressure"), 'T', TN2start, "N2")
rhoN2LowStart = cp.PropsSI('D', 'P', convertToSI(1350, "psi", "pressure"), 'T', TN2start, "N2")
rhoN2HighEnd = cp.PropsSI('D', 'P', convertToSI(1600, "psi", "pressure"), 'T', TN2HighEnd, "N2")
rhoN2LowEnd = cp.PropsSI('D', 'P', convertToSI(1350, "psi", "pressure"), 'T', TN2LowEnd, "N2")
RN2 = 8314 / 28.02

#all the fixed mass of the rocket
fixedRocketMass = 43.462 * 1.1 #current mass budget value + 10 % allowance

#parameters
burnTime = 3
TWR = 8
OF = 4.9705
expansionRatio = 9.155864715576172
chamberPressure = 809.9529469
g = 9.81
ullage = 0.15

#efficiency factors
CStar = 0.85
Nozzle = 0.95

C = CEA_Obj(oxName='N2O', fuelName='ETHANOL')

VeFrozen = C.get_SonicVelocities(Pc=chamberPressure, MR=OF, eps=expansionRatio, frozen=0, frozenAtThroat=0)[2]
VeEquil = C.get_SonicVelocities(Pc=chamberPressure, MR=OF, eps=expansionRatio, frozen=1, frozenAtThroat=1)[2]
Ve = (VeFrozen + VeEquil) / 2 #exit velocity, thrust per propellant flow rate
Ve = Ve * CStar * Nozzle # Efficiency knockdown factors

def getVariableMass(rocketMass):
    thrust = rocketMass * g * TWR
    mProp = thrust / Ve * 3 #amount of propellant for 3 second burn
    mFuel = mProp / (1 + OF)
    mOx = OF * mFuel

    vFuel = mFuel / rhoFuel #volume of fuel, assuming 880 kg/m^3 density, no ullage
    fuelTankMass = FuelPVMass(vFuel)

    deadVolume = FuelDeadVolume(vFuel) #volume occupied by fuel tank in nitrous tank.

    vOx = (mOx / rhoNOS)
    vUllage = ullage * (vOx / (1 - ullage))
    vTank = vOx + vUllage
    vTank = vTank + deadVolume

    oxTankMass = NOSPVMass(vTank)
    
    ullageMass = rhoN2LowStart * vUllage

    endN2MassLow = rhoN2LowEnd * (vTank - deadVolume)
    N2Used = endN2MassLow - ullageMass

    PTTerm = TN2HighEnd/TN2start * PN2HighStart/PN2HighEnd
    N2MassInitial = N2Used * PTTerm / (PTTerm - 1)
    
    VN2 = N2MassInitial * RN2 * TN2start / convertToSI(PN2HighStart, "psi", "pressure")
    N2TankMass = N2PVMass(VN2)
    N2TubeMass = N2AirframeMass(VN2)

    N2MassFinal = N2MassInitial - N2Used
    
    variableMass = N2TubeMass + N2MassInitial + N2TankMass + mFuel + fuelTankMass + oxTankMass + mOx + ullageMass

    return variableMass

variableMass = getVariableMass(fixedRocketMass)

mass = []
thrust = []
n = []

"""Finding rocket mass / thrust requirement
for i in range(100):
    variableMass = getVariableMass(fixedRocketMass + variableMass)
    mass.append(variableMass + fixedRocketMass)
    thrust.append(g * (fixedRocketMass + variableMass) * TWR)
    n.append(i)

"""

''' plotting convergence of thrust, rocket mass.
fig, ax = plt.subplots()

ax.plot(n, thrust)
ax.set_ylabel("Thrust (N)")
ax.set_xlabel("Iterations")
plt.show()
'''

def rocketDesign(thrust):
    print("Design thrust: %.4s N" %thrust)
    mProp = thrust / Ve * 3 #amount of propellant for 3 second burn
    print("Propellant mass: %.4s kg" %mProp)
    print("Propellant mass flow rate: %.4s kg/s" %(mProp  / 3))
    mFuel = mProp / (1 + OF)
    print("Fuel mass: %.4s kg" %mFuel)
    print("Fuel mass flow rate: %.4s kg/s" %(mFuel / 3))
    mOx = OF * mFuel
    print("NOS mass: %.4s kg" %mOx)
    print("NOS mass flow rate: %.4s kg/s" %(mOx / 3))

    vFuel = mFuel / rhoFuel #volume of fuel, assuming 880 kg/m^3 density, no ullage
    fuelTankMass, fuelPVLength = FuelPVMass(vFuel)

    deadVolume = FuelDeadVolume(vFuel) #volume occupied by fuel tank in nitrous tank.

    vOx = (mOx / rhoNOS)
    vUllage = ullage * (vOx / (1 - ullage))
    vTank = vOx + vUllage
    vTank = vTank + deadVolume

    oxTankMass, NOSPVLength = NOSPVMass(vTank)
    
    ullageMass = rhoN2LowStart * vUllage

    endN2MassLow = rhoN2LowEnd * (vTank - deadVolume)
    N2Used = endN2MassLow - ullageMass

    PTTerm = TN2HighEnd/TN2start * PN2HighStart/PN2HighEnd
    N2MassInitial = N2Used * PTTerm / (PTTerm - 1)
    
    VN2 = N2MassInitial * RN2 * TN2start / convertToSI(PN2HighStart, "psi", "pressure")
    N2TankMass, N2PVLength = N2PVMass(VN2)
    N2TubeMass = N2AirframeMass(VN2)

    print("\nNOS PV Length: %.4f m" %NOSPVLength)
    print("Fuel PV Length: %.4f m" %fuelPVLength)
    print("N2 PV Length: %.4f m" %N2PVLength)
    N2MassFinal = N2MassInitial - N2Used
    
    variableMass = N2TubeMass + N2MassInitial + N2TankMass + mFuel + fuelTankMass + oxTankMass + mOx + ullageMass

rocketDesign(5500)