from functions.units import *
from classes.State import *

class Tank:
    volume = 0 #total volume of rigid tank, in m3
    liquid = "" #state object of the liquid phase in the tank

    def __init__(self):
        pass

    def load(self, dic):
        self.volume = convertToSI(dic["volume"], dic["volumeUnit"], "volume")
        self.liquid = State()
        self.liquid.load(dic["liquid"])
