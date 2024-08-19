from classes.Tank import *

class Engine:
    oxTank = "" #instance of class tank

    def __init__(self):
        pass

    def load(self, dic):
        self.oxTank = Tank()
        self.oxTank.load(dic["oxTank"])