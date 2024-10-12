from functions.fileIO import *
from classes.OxTank import *
from classes.PressTank import *
from classes.State import *
from classes.Engine import *
from classes.EndConditions import * 
from classes.Plotter import *

#dic = LoadJSON("simDefs/default.json") # Original data file that Lukas' created
dic = LoadJSON("simDefs/defs_oct11.json") # Mass budget values as of Oct. 11, 2024 (https://docs.google.com/spreadsheets/d/18GnIIEJeY7-gzHpHSoPhtmgDRNokLcbnRhNP7b0LVrU/edit?gid=879026709#gid=879026709)

#option to toggle simulation and plots
#note: if an error occurs from the simulation, 
#      you can disable sims the second time around 
#      and run plots option only to display data.

RUN_SIM = False
SHOW_PLOTS = True

if RUN_SIM:
    engine = Engine()
    engine.Load(dic)
    engine.runSim()

if SHOW_PLOTS:
    p = Plotter("log.csv")
    p.load_data()
    #each instance of .plot_columns, a new figure will be displayed
    p.plot_columns(["engine.oxTank.liquid.mass", "engine.oxTank.gas.mass", "engine.pressTank.gas.mass", "engine.fuelTank.liquid.mass"])
    p.plot_columns(["engine.oxTank.gas.pressure", "engine.pressTank.gas.pressure", "engine.fuelTank.liquid.pressure"])
    p.show_all()