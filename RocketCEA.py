# import matplotlib.pyplot as plt
# from rocketcea.cea_obj import CEA_Obj, add_new_fuel

# # Define a new fuel card for B100
# card_str = """
# name B100 C 19 H 38 O 2  wt%=100.00
# h,cal=-162.59321214343998    t(k)=288.15  rho=806
# """
# add_new_fuel('B100', card_str)

# # Initialize the CEA instances for each propellant combination
# isp_calculator = CEA_Obj(oxName='N2O', fuelName='ETHANOL')
# new_propellant_calculator = CEA_Obj(oxName='N2O', fuelName='B100')

# # Set O/F ratio range
# of_ratios = [i * 0.5 for i in range(4, 21)]  # Generates O/F ratios from 2 to 10

# # Initialize lists to store data
# n2o_ethanol_temps = []
# n2o_ethanol_isp_grav = []
# new_propellant_temps = []
# new_propellant_isp_grav = []

# # Gravity constant
# g = 9.81
# p_c = 812  # Chamber pressure in psi
# eps = 9.156  # Expansion ratio

# # Iterate through O/F ratios for N2O and Ethanol
# for of_ratio in of_ratios:
#     temp = isp_calculator.get_Temperatures(Pc=p_c, MR=of_ratio, eps=eps, frozen=0, frozenAtThroat=0)[0]  # Correct order
#     isp = isp_calculator.get_Isp(p_c, of_ratio, eps)  # Use positional arguments
#     n2o_ethanol_temps.append(temp)
#     n2o_ethanol_isp_grav.append(isp)

# # Iterate through O/F ratios for the new propellant
# for of_ratio in of_ratios:
#     temp = new_propellant_calculator.get_Temperatures(Pc=p_c, MR=of_ratio, eps=eps, frozen=0, frozenAtThroat=0)[0]
#     isp = new_propellant_calculator.get_Isp(p_c, of_ratio, eps)  # Use positional arguments
#     new_propellant_temps.append(temp)
#     new_propellant_isp_grav.append(isp)

# # Plot results
# plt.figure(figsize=(10, 6))
# plt.plot(of_ratios, n2o_ethanol_temps, label='N2O + Ethanol Temperature', marker='o')
# plt.plot(of_ratios, new_propellant_temps, label='N2O + B100 Temperature', marker='x')
# plt.xlabel('O/F Ratio')
# plt.ylabel('Temperature (K)')
# plt.title('Temperature vs O/F Ratio')
# plt.legend()
# plt.grid()

# plt.figure(figsize=(10, 6))
# plt.plot(of_ratios, n2o_ethanol_isp_grav, label='N2O + Ethanol Isp / g', marker='o')
# plt.plot(of_ratios, new_propellant_isp_grav, label='N2O + B100 Isp / g', marker='x')
# plt.xlabel('O/F Ratio')
# plt.ylabel('Isp / g (s)')
# plt.title('Isp / g vs O/F Ratio')
# plt.legend()
# plt.grid()

# plt.show()

import matplotlib.pyplot as plt
from rocketcea.cea_obj import CEA_Obj, add_new_fuel
import numpy as np

# Define a new fuel card for B100
card_str = """
name B100 C 19 H 38 O 2  wt%=100.00
h,cal=-226,000    t(k)=288.15  rho=820
"""
add_new_fuel('B100', card_str)

# Initialize the CEA instances for each propellant combination
# Initialize the CEA instances for each propellant combination
isp_calculator = CEA_Obj(oxName='N2O', fuelName='C2H5OH')
new_propellant_calculator = CEA_Obj(oxName='N2O', fuelName='B100')


# Set O/F ratio range
of_ratios = [i * 0.5 for i in range(4, 21)]  # Generates O/F ratios from 2 to 10

# Initialize lists to store data
n2o_ethanol_temps = []
n2o_ethanol_isp = []
new_propellant_temps = []
new_propellant_isp = []
n2o_ethanol_L_star = []
new_propellant_L_star = []

# Constants for characteristic length calculation
p_c = 812  # Chamber pressure in psi
eps = 9.156  # Expansion ratio
A_t = 0.01  # Example throat area in m² (adjust as needed)

# Iterate through O/F ratios for N2O and Ethanol
for of_ratio in of_ratios:
    temp = isp_calculator.get_Temperatures(Pc=p_c, MR=of_ratio, eps=eps, frozen=0, frozenAtThroat=1)[0]
    isp = isp_calculator.get_Isp(p_c, of_ratio, eps)
    V_c = (isp * 1000) / (p_c * 6.89476)  # Example calculation, adjust as needed
    L_star = V_c / A_t  # Characteristic length calculation
    n2o_ethanol_temps.append(temp)
    n2o_ethanol_isp.append(isp)
    n2o_ethanol_L_star.append(L_star)

# Iterate through O/F ratios for the new propellant
for of_ratio in of_ratios:
    temp = new_propellant_calculator.get_Temperatures(Pc=p_c, MR=of_ratio, eps=eps, frozen=0, frozenAtThroat=1)[0]
    isp = new_propellant_calculator.get_Isp(p_c, of_ratio, eps)
    V_c = (isp * 1000) / (p_c * 6.89476)  # Example calculation, adjust as needed
    L_star = V_c / A_t  # Characteristic length calculation
    new_propellant_temps.append(temp)
    new_propellant_isp.append(isp)
    new_propellant_L_star.append(L_star)

# Plot results
plt.figure(figsize=(12, 8))

# Plot Temperatures
plt.subplot(3, 1, 1)
plt.plot(of_ratios, n2o_ethanol_temps, label='N2O + Ethanol Temperature (K)', marker='o')
plt.plot(of_ratios, new_propellant_temps, label='N2O + B100 Temperature (K)', marker='x')
plt.xlabel('O/F Ratio')
plt.ylabel('Temperature (K)')
plt.title('Temperature vs O/F Ratio')
plt.legend()
plt.grid()

# Plot Isp
plt.subplot(3, 1, 2)
plt.plot(of_ratios, n2o_ethanol_isp, label='N2O + Ethanol Isp (s)', marker='o')
plt.plot(of_ratios, new_propellant_isp, label='N2O + B100 Isp (s)', marker='x')
plt.xlabel('O/F Ratio')
plt.ylabel('Isp (s)')
plt.title('Isp vs O/F Ratio')
plt.legend()
plt.grid()

# Plot Characteristic Length
plt.subplot(3, 1, 3)
plt.plot(of_ratios, n2o_ethanol_L_star, label='N2O + Ethanol L* (m)', marker='o')
plt.plot(of_ratios, new_propellant_L_star, label='N2O + B100 L* (m)', marker='x')
plt.xlabel('O/F Ratio')
plt.ylabel('Characteristic Length L* (m)')
plt.title('Characteristic Length vs O/F Ratio')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
