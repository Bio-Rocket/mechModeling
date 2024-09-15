from classes.OxTank import *
from classes.PressurantTank import *
from classes.EndConditions import *
from classes.SimControl import *
from classes.Parameters import *

import pandas as pd
import numpy as np

class Pressurization:
    oxTank = "" #instance of class tank
    endConditions = "" #instance of class EndConditions
    simControl = "" #instance of class simControl
    parameters = "" #instance of class parameters
    log = "" #dataFrame tracking simulation values

    def __init__(self):
        pass

    #fanno flow function
    #inputs:
    #
    def FannoTimize(Ti, To, friction):
        pass