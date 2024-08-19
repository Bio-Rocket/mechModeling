from functions.fileIO import *
from classes.Tank import *
from classes.State import *
from classes.Engine import *
from classes.EndConditions import *

dic = LoadJson("simDefs/default.json")

engine = Engine()
engine.Load(dic)

engine.drainOxTank()

print(engine.log)