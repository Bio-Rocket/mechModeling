from functions.fileIO import *
from classes.OxTank import *
from classes.PressTank import *
from classes.State import *
from classes.Engine import *
from classes.EndConditions import *
from classes.Plotter import *

SHOW_PLOTS = True

#dic = LoadJSON("simDefs/default.json") # Original data file that Lukas' created
dic = LoadJSON("simDefs/default.json") # Mass budget values as of Sept. 15, 2024 (https://docs.google.com/spreadsheets/d/18GnIIEJeY7-gzHpHSoPhtmgDRNokLcbnRhNP7b0LVrU/edit?gid=879026709#gid=879026709)

engine = Engine()
engine.Load(dic)

engine.RegulatorBlowDown()

if SHOW_PLOTS:
    p = Plotter("log.csv")
    p.load_data()
    #each instance of .plot_columns, a new figure will be displayed
    #flow rate plot
    p.plot_columns(["engine.pressTank.pressurantMassFlowRate","engine.pressTank.pressurantMassFlowRateFuel","engine.pressTank.pressurantMassFlowRateOx"], override_title="N2 Flow Rates", override_x_label="Time (s)", override_y_label="Mass Flow Rate N2 (kg/s)")

    #mass plot
    #p.plot_columns(["engine.oxTank.liquid.mass", "engine.oxTank.gas.mass", "engine.pressTank.gas.mass", "engine.fuelTank.liquid.mass"])
    
    #pressure plot
    #p.plot_columns(["engine.oxTank.gas.pressure"], override_title="EPR Controlled Pressure", override_x_label="Time (s)", override_y_label="Propellant Pressure (Pa)")

    #temperature plot
    #p.plot_columns(["engine.oxTank.gas.temperature", "engine.pressTank.gas.temperature", "engine.fuelTank.liquid.temperature"])
    p.show_all()