from classes.State import *
from functions.units import *
import math as m

ambientPressure = convertToSI(14, "psi", "pressure")
ambientTemperature = convertToSI(15, "C", "temperature")
gas = 'N2'

PLoss_UPSTREAM = 0
PLoss_DOWNSTREAM_OX = 0
PLoss_DOWNSTREAM_FUEL = 0

P_UPSTREAM = 5880
P_DOWNSTREAM = 1350

N2_UPSTREAM = State()
N2_UPSTREAM.fluid = gas
N2_UPSTREAM.temperature = convertToSI(15, "C", "temperature")
N2_UPSTREAM.pressure = convertToSI(P_UPSTREAM, "psi", "pressure")
N2_UPSTREAM.SetIntrinsicProperties("temperature", N2_UPSTREAM.temperature, "pressure", N2_UPSTREAM.pressure)

N2_DOWNSTREAM = State()
N2_DOWNSTREAM.fluid = gas
N2_DOWNSTREAM.temperature = convertToSI(15, "C", "temperature")
N2_DOWNSTREAM.pressure = convertToSI(P_DOWNSTREAM, "psi", "pressure")
N2_DOWNSTREAM.SetIntrinsicProperties("temperature", N2_DOWNSTREAM.temperature, "pressure", N2_DOWNSTREAM.pressure)

# relative roughness
# reference: Fundamentals of Fluid Mechanics by Rothmayer
# assuming line pipe
ROUGHNESS = 0.0000015 # drawn tubing, 0.0015mm

# Mass flow rate of N2
MASSRATE_UPSTREAM = 2.010135650634765
MASSRATE_DOWNSTREAM_OX = 1.6023980054800484	 
MASSRATE_DOWNSTREAM_FUEL = 0.40773764515471717
print(f"[m] Mass Flow, U.S.: {MASSRATE_UPSTREAM:.2f}kg/s, D.S.Ox: {MASSRATE_DOWNSTREAM_OX:.2f}kg/s, D.S.Fuel: {MASSRATE_DOWNSTREAM_FUEL:.2f}kg/s")

# Length of tubing
L_UPSTREAM = 0.938 + 9.577 + 0.66 + 3.846 + 1.5 + 1.5 + 1.5 #inches
L_UPSTREAM = convertToSI(L_UPSTREAM, "in", "length")
L_DOWNSTREAM_OX = 1.5 + 5.308 + 3.807 + 70.169 + 0.9 + 0.9 + 7.224 + 1.188
L_DOWNSTREAM_OX  = convertToSI(L_DOWNSTREAM_OX , "in", "length")
L_DOWNSTREAM_FUEL_1 = 1.5 +  6.325
L_DOWNSTREAM_FUEL_1 = convertToSI(L_DOWNSTREAM_FUEL_1, "in", "length")
L_DOWNSTREAM_FUEL_2 = 0.64 + 3 + 3.427 + 0.6 + 6.976 + 0.813
L_DOWNSTREAM_FUEL_2 = convertToSI(L_DOWNSTREAM_FUEL_2, "in", "length")

# Number of fittings and their corresponding loss coefficient, K
# UPSTREAM 3/8"
# Contraction, 3.5" to 3/8" -> 0.975
# Straight Fitting, 0.08
# 90-degree Elbow, 0.3
# 4x Straight Fitting, 0.32
# 90-degree Elbow, 0.3
# Cross-straight, 0.15
# Ball valve open, 0.05
# T-straight, 0.7
# Straight fitting, 0.08

# DOWNSTREAM NOS 1/2"
# Straight fitting, 0.08
# Cross 90-degree, 1.1
# Ball valve open, 0.05
# Cross with 90-degree, 1.1
# 90-degree, 0.3
# 90-degree, 0.3
# Straight fitting, 0.08
# Gradual expansion, 0.158

# DOWNSTREAM FUEL 1/2"
# Straight fitting, 0.08
# Cross 90-degree, 1.1
# Reduction for Fuel, 0.639

# DOWNSTREAM FUEL 1/4"
# 1/4 ball valve open, 0.2
# Cross 90-degree, 1.1
# 90-degree, 0.3
# 90-degree, 0.3
# Straight fitting, 0.08
# Expansion, 0.9947

FITTINGS_UPSTREAM = [0.975, 0.08, 0.3, 0.32, 0.3, 0.15, 0.05, 0.7, 0.08]
FITTINGS_DOWNSTREAM_OX = [0.08, 1.1, 0.05, 1.1, 0.3, 0.3, 0.08, 0.158]
FITTINGS_DOWNSTREAM_FUEL_1 = [0.08, 1.1, 0.639]
FITTINGS_DOWNSTREAM_FUEL_2 = [0.2, 1.1, 0.3, 0.3, 0.08, 0.9947]

# 1/4" upstream tubing, thickness 0.049"
# 1/2" downstream tubing, thickness 0.083"
ID_3_8 = convertToSI(3/8 - 0.065 * 2, "in", "length") # 3/8" tubing for 5880 PSI
A_3_8 = ID_3_8 ** 2 * m.pi / 4

ID_1_4 = convertToSI(1/4 - 0.028 * 2, "in", "length") # 1/4" tubing for 1350 PSI
A_1_4 = ID_1_4 ** 2 * m.pi / 4
ID_1_2 = convertToSI(1/2 - 0.035 * 2, "in", "length") # 1/2" tubing for 1350 PSI
A_1_2 = ID_1_2 ** 2 * m.pi / 4

FLOWRATE_UPSTREAM = MASSRATE_UPSTREAM / N2_UPSTREAM.density
FLOWRATE_DOWNSTREAM_OX = MASSRATE_DOWNSTREAM_OX / N2_DOWNSTREAM.density
FLOWRATE_DOWNSTREAM_FUEL_1 = MASSRATE_DOWNSTREAM_FUEL / N2_DOWNSTREAM.density
FLOWRATE_DOWNSTREAM_FUEL_2 = MASSRATE_DOWNSTREAM_FUEL / N2_DOWNSTREAM.density
print(f"[Q] Flow Rate, U.S.: {FLOWRATE_UPSTREAM:.6f}m^3/s, D.S.Ox(3/8\"): {FLOWRATE_DOWNSTREAM_OX:.6f}m^3/s, D.S.Fuel(1/2\"): {FLOWRATE_DOWNSTREAM_FUEL_1:.6f}m^3/s, D.S.Fuel(1/4\"): {FLOWRATE_DOWNSTREAM_FUEL_2:.6f}m^3/s")

VELOCITY_UPSTREAM = FLOWRATE_UPSTREAM / A_3_8
VELOCITY_DOWNSTREAM_OX = FLOWRATE_DOWNSTREAM_OX / A_1_2
VELOCITY_DOWNSTREAM_FUEL_1 = FLOWRATE_DOWNSTREAM_FUEL_1 / A_1_2
VELOCITY_DOWNSTREAM_FUEL_2 = FLOWRATE_DOWNSTREAM_FUEL_2 / A_1_4

print(f"[v] Velocity, U.S.(3/8\"): {VELOCITY_UPSTREAM:.2f}m/s, D.S.(1/2\"): {VELOCITY_DOWNSTREAM_OX:.2f}m/s, D.S.(1/2\"): {VELOCITY_DOWNSTREAM_FUEL_1:.2f}m/s, D.S.(1/4\"): {VELOCITY_DOWNSTREAM_FUEL_2:.2f}m/s")

# Reynolds Number
Re_UPSTREAM = N2_UPSTREAM.density * VELOCITY_UPSTREAM * ID_3_8 / N2_UPSTREAM.dynamicViscosity
Re_DOWNSTREAM_OX = N2_DOWNSTREAM.density * VELOCITY_DOWNSTREAM_OX * ID_1_2 / N2_DOWNSTREAM.dynamicViscosity
Re_DOWNSTREAM_FUEL_1 = N2_DOWNSTREAM.density * VELOCITY_DOWNSTREAM_FUEL_1 * ID_1_2 / N2_DOWNSTREAM.dynamicViscosity
Re_DOWNSTREAM_FUEL_2 = N2_DOWNSTREAM.density * VELOCITY_DOWNSTREAM_FUEL_2 * ID_1_4 / N2_DOWNSTREAM.dynamicViscosity

PLoss_FITTINGS_UPSTREAM = 0
PLoss_FITTINGS_DOWNSTREAM_OX = 0
PLoss_FITTINGS_DOWNSTREAM_FUEL_1 = 0
PLoss_FITTINGS_DOWNSTREAM_FUEL_2 = 0

PLoss_FITTINGS_UPSTREAM = sum(K * (N2_UPSTREAM.density * VELOCITY_UPSTREAM ** 2) / (2) for K in FITTINGS_UPSTREAM)
PLoss_FITTINGS_UPSTREAM_IMPERIAL = PLoss_FITTINGS_UPSTREAM / convertToSI(1, "psi", "pressure")
PLoss_FITTINGS_DOWNSTREAM_OX = sum(K * (N2_DOWNSTREAM.density * VELOCITY_DOWNSTREAM_OX ** 2) / (2) for K in FITTINGS_DOWNSTREAM_OX)
PLoss_FITTINGS_DOWNSTREAM_OX_IMPERIAL = PLoss_FITTINGS_DOWNSTREAM_OX / convertToSI(1, "psi", "pressure")
PLoss_FITTINGS_DOWNSTREAM_FUEL_1 = sum(K * (N2_DOWNSTREAM.density * VELOCITY_DOWNSTREAM_FUEL_1 ** 2) / (2) for K in FITTINGS_DOWNSTREAM_FUEL_1)
PLoss_FITTINGS_DOWNSTREAM_FUEL_1_IMPERIAL = PLoss_FITTINGS_DOWNSTREAM_FUEL_1 / convertToSI(1, "psi", "pressure")
PLoss_FITTINGS_DOWNSTREAM_FUEL_2 = sum(K * (N2_DOWNSTREAM.density * VELOCITY_DOWNSTREAM_FUEL_2 ** 2) / (2) for K in FITTINGS_DOWNSTREAM_FUEL_2)
PLoss_FITTINGS_DOWNSTREAM_FUEL_2_IMPERIAL = PLoss_FITTINGS_DOWNSTREAM_FUEL_2 / convertToSI(1, "psi", "pressure")

print(f"Pressure Loss due to fittings U.S.(3/8\"): {PLoss_FITTINGS_UPSTREAM_IMPERIAL:.2f}PSI, D.S.Ox(1/2\"): {PLoss_FITTINGS_DOWNSTREAM_OX_IMPERIAL:.2f}PSI, D.S.Fuel(1/2\"): {PLoss_FITTINGS_DOWNSTREAM_FUEL_1_IMPERIAL:.2f}PSI, D.S.Fuel(1/4\"): {PLoss_FITTINGS_DOWNSTREAM_FUEL_2_IMPERIAL:.2f}PSI")


f_UPSTREAM = 0.25 / (m.log10((ROUGHNESS / ID_3_8) / 3.7 + 5.74 / (Re_UPSTREAM ** 0.9))) ** 2
PLoss_FRICTION_UPSTREAM = (f_UPSTREAM * N2_UPSTREAM.density * L_UPSTREAM * VELOCITY_UPSTREAM ** 2) / (2 * ID_3_8)
PLoss_FRICTION_UPSTREAM_IMPERIAL = PLoss_FRICTION_UPSTREAM / convertToSI(1, "psi", "pressure")

f_DOWNSTREAM_OX = 0.25 / (m.log10((ROUGHNESS / ID_1_2) / 3.7 + 5.74 / (Re_DOWNSTREAM_OX ** 0.9))) ** 2
PLoss_FRICTION_DOWNSTREAM_OX = (f_DOWNSTREAM_OX * N2_DOWNSTREAM.density * L_DOWNSTREAM_OX * VELOCITY_DOWNSTREAM_OX ** 2) / (2 * ID_1_2)
PLoss_FRICTION_DOWNSTREAM_OX_IMPERIAL = PLoss_FRICTION_DOWNSTREAM_OX / convertToSI(1, "psi", "pressure")

f_DOWNSTREAM_FUEL_1 = 0.25 / (m.log10((ROUGHNESS / ID_1_2) / 3.7 + 5.74 / (Re_DOWNSTREAM_FUEL_1 ** 0.9))) ** 2
PLoss_FRICTION_DOWNSTREAM_FUEL_1 = (f_DOWNSTREAM_FUEL_1 * N2_DOWNSTREAM.density * L_DOWNSTREAM_FUEL_1 * VELOCITY_DOWNSTREAM_FUEL_1 ** 2) / (2 * ID_1_2)
PLoss_FRICTION_DOWNSTREAM_FUEL_1_IMPERIAL = PLoss_FRICTION_DOWNSTREAM_FUEL_1 / convertToSI(1, "psi", "pressure")

f_DOWNSTREAM_FUEL_2 = 0.25 / (m.log10((ROUGHNESS / ID_1_2) / 3.7 + 5.74 / (Re_DOWNSTREAM_FUEL_2 ** 0.9))) ** 2
PLoss_FRICTION_DOWNSTREAM_FUEL_2 = (f_DOWNSTREAM_FUEL_2 * N2_DOWNSTREAM.density * L_DOWNSTREAM_FUEL_2 * VELOCITY_DOWNSTREAM_FUEL_2 ** 2) / (2 * ID_1_2)
PLoss_FRICTION_DOWNSTREAM_FUEL_2_IMPERIAL = PLoss_FRICTION_DOWNSTREAM_FUEL_2 / convertToSI(1, "psi", "pressure")
print(f"Pressure Loss due to friction U.S.(1/4\"): {PLoss_FRICTION_UPSTREAM_IMPERIAL:.2f}PSI, D.S.OX(1/2\"): {PLoss_FRICTION_DOWNSTREAM_OX_IMPERIAL:.2f}PSI, D.S.FUEL(1/2\"): {PLoss_FRICTION_DOWNSTREAM_FUEL_1_IMPERIAL:.2f}PSI, D.S.FUEL(1/4\"): {PLoss_FRICTION_DOWNSTREAM_FUEL_2_IMPERIAL:.2f}PSI")

PLoss_UPSTREAM += PLoss_FITTINGS_UPSTREAM + PLoss_FRICTION_UPSTREAM
PLoss_DOWNSTREAM_OX += PLoss_FITTINGS_DOWNSTREAM_OX + PLoss_FRICTION_DOWNSTREAM_OX
PLoss_DOWNSTREAM_FUEL += PLoss_FITTINGS_DOWNSTREAM_FUEL_1 + PLoss_FRICTION_DOWNSTREAM_FUEL_1 + PLoss_FITTINGS_DOWNSTREAM_FUEL_2 + PLoss_FRICTION_DOWNSTREAM_FUEL_2

PLoss_UPSTREAM_IMPERIAL = PLoss_FITTINGS_UPSTREAM_IMPERIAL + PLoss_FRICTION_UPSTREAM_IMPERIAL#PLoss_UPSTREAM / convertToSI(1, "psi", "pressure")
PLoss_DOWNSTREAM_OX_IMPERIAL = PLoss_FITTINGS_DOWNSTREAM_OX_IMPERIAL + PLoss_FRICTION_DOWNSTREAM_OX_IMPERIAL
PLoss_DOWNSTREAM_FUEL_IMPERIAL = PLoss_FITTINGS_DOWNSTREAM_FUEL_1_IMPERIAL + PLoss_FRICTION_DOWNSTREAM_FUEL_1_IMPERIAL + PLoss_FITTINGS_DOWNSTREAM_FUEL_2_IMPERIAL + PLoss_FRICTION_DOWNSTREAM_FUEL_2_IMPERIAL

P_UPSTREAM_FINAL = P_UPSTREAM - PLoss_UPSTREAM_IMPERIAL
P_DOWNSTREAM_OX_FINAL = P_DOWNSTREAM - PLoss_DOWNSTREAM_OX_IMPERIAL
P_DOWNSTREAM_FUEL_FINAL = P_DOWNSTREAM - PLoss_DOWNSTREAM_FUEL_IMPERIAL

#print("[dP] Pressure Loss, Imperial\nUpstream: ", PLoss_UPSTREAM_IMPERIAL, "[Psi]\nDownstream: ", PLoss_DOWNSTREAM_IMPERIAL,"[Psi]")
print(f"UPSTREAM (1/4\"): Initial: {P_UPSTREAM:.0f}PSI -> Final: {P_UPSTREAM_FINAL:.2f}PSI (-{PLoss_UPSTREAM_IMPERIAL:.0f}) @ {MASSRATE_UPSTREAM:.3f}kg/s")
print(f"DOWNSTREAM OX (1/2\"): Initial: {P_DOWNSTREAM:.0f}PSI -> Final: {P_DOWNSTREAM_OX_FINAL:.2f}PSI (-{PLoss_DOWNSTREAM_OX_IMPERIAL:.0f}) @ {MASSRATE_DOWNSTREAM_OX:.3f}kg/s")
print(f"DOWNSTREAM FUEL (1/2 -> 1/4\"): Initial: {P_DOWNSTREAM:.0f}PSI -> Final: {P_DOWNSTREAM_FUEL_FINAL:.2f}PSI (-{PLoss_DOWNSTREAM_FUEL_IMPERIAL:.0f}) @ {MASSRATE_DOWNSTREAM_FUEL:.3f}kg/s")



