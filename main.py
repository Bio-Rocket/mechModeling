from functions.fileIO import *
from classes.OxTank import *
from classes.PressTank import *
from classes.State import *
from classes.Engine import *
from classes.EndConditions import *

dic = LoadJson("simDefs/default.json")

engine = Engine()
engine.Load(dic)

engine.drainTanks()

print(engine.log)