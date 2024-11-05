from functions.fileIO import *
from classes.OxTank import *
from classes.PressTank import *
from classes.State import *
from classes.Engine import *
from classes.EndConditions import *
from classes.Plotter import *

#dic = LoadJSON("simDefs/default.json") # Original data file that Lukas' created
dic = LoadJSON("simDefs/updatedInputs.json") # Mass budget values as of Sept. 15, 2024 (https://docs.google.com/spreadsheets/d/18GnIIEJeY7-gzHpHSoPhtmgDRNokLcbnRhNP7b0LVrU/edit?gid=879026709#gid=879026709)
SHOW_PLOTS = True
RUN_SIM = False
if RUN_SIM:
    try:
        engine = Engine()
        engine.Load(dic)

        engine.runSim()
    except:
        "Error trying to conclude Simulation, continuing..."

if SHOW_PLOTS:
    #p = Plotter("logBlowDown.csv")
    p = Plotter("log_backup_with_solenoid_data.csv")
    p.load_data()
    #each instance of .plot_columns, a new figure will be displayed
    #mass plot
    #p.plot_columns(["engine.oxTank.liquid.mass", "engine.oxTank.gas.mass", "engine.pressTank.gas.mass", "engine.fuelTank.liquid.mass"])
    
    #pressure plot
    #p.plot_columns(["engine.oxTank.gas.pressure"], override_title="EPR Controlled Pressure", override_x_label="Time (s)", override_y_label="Propellant Pressure (Pa)")
    p.plot_columns(["bigGems_Open","bigGems_Close"], override_title="Large Solenoid Actuation Test (DG2002-01LB-V-G5-203)", override_x_label="Trial #", override_y_label="Delay (ms)", connect_data=False,x_major_unit=1, y_axis_limits=(0, 180))
    p.plot_columns(["smallGems_Open","smallGems_Close"], override_title="Small Solenoid Actuation Test (A2011-V-VO-C203)", override_x_label="Trial #", override_y_label="Delay (ms)", connect_data=False, x_major_unit=1, y_axis_limits=(0, 20))
    #p.plot_columns(["Blowdown","EPR","MPR"], override_title="Pressure Control Methods", override_x_label="Time (s)", override_y_label="Pressure (psi)",x_major_unit=0.25)

    #temperature plot
    #p.plot_columns(["engine.oxTank.gas.temperature", "engine.pressTank.gas.temperature", "engine.fuelTank.liquid.temperature"])

    p.show_all()