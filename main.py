from functions.fileIO import *
from classes.OxTank import *
from classes.PressTank import *
from classes.State import *
from classes.Engine import *
from classes.EndConditions import *

#dic = LoadJSON("simDefs/default.json") # Original data file that Lukas' created
dic = LoadJSON("simDefs/mass budget_09-15-2024.json") # Mass budget values as of Sept. 15, 2024 (https://docs.google.com/spreadsheets/d/18GnIIEJeY7-gzHpHSoPhtmgDRNokLcbnRhNP7b0LVrU/edit?gid=879026709#gid=879026709)

engine = Engine()

engine.drainTanks()

engine.LoadPressurant(dic)
engine.drainPressurantTank()
print(engine.log_pressurant)