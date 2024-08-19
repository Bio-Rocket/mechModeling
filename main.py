from functions.fileIO import *
from classes.Tank import *
from classes.State import *
from classes.Engine import *

import pandas as pd

dic = LoadJson("simDefs/default.json")

engine = Engine()
engine.load(dic)

print(engine.oxTank.volume)
log = pd.DataFrame()