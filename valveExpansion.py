from classes.State import *
from functions.units import *

ambientPressure = convertToSI(14, "psi", "pressure")
tankState = State()

tankState.fluid = "N2"
tankState.temperature = convertToSI(20, "C", "temperature")
tankState.pressure = convertToSI(5800, "psi", "pressure")
tankState.SetIntrinsicProperties("temperature", tankState.temperature, "pressure", tankState.pressure)

linePressure = convertToSI(1350, "psi", "pressure")
outletTemperature = tankState.IsentropicPressureChange(linePressure)
print(outletTemperature - 273.15)