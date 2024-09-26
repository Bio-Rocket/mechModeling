class Control:
    #constant
    openDelay = 0 #The delay between energizing coil and fully open valve, in s.
    closeDelay = 0 #The delay between de-energizing coil and fully closed valve, in s.

    #variables
    opened = False #The state of the valve, True or False
    energized = False #The state of the coil, True or False

    lowThreshold = 0 #The pressure at which to open the valve, in Pa
    setPoint = 0 #The ideal pressure for the system to operate at, in Pa
    highThreshold = 0 #The pressure at which to close the valve, in Pa

    timeCoilCycled = 0 #The time at which the state of the coil last changed, in s
    timeValveCycled = 0 #The time at which the state of the valve last changed, in s

    def __init__(self):
        pass

    def DetermineState(self, oxPressure, currentTime):
        
        #in this case, the valve needs to be opened
        if oxPressure < lowThreshold:

            #the valve is still closed, need to open it.
            if not self.opened:
                
                #If the valve is being opened already, keep opening it, but check if it has opened fully.
                if self.energized:
                    if currentTime - self.timeCoilCycled >= self.openDelay:
                        self.opened = True
                        self.timeValveCycled = currentTime

                #The pressure is below threshold, the valve is not yet open, and not yet energized, therefore, energize it.
                else:
                    self.energized = True
                    self.timeCoilCycled = currentTime

        #in this case, the valve needs to be closed. 
        if oxPressure > highThreshold:

            #if the valve is still open, need to close it. 
            if self.open:

                #if the valve is open and still energized, de-energize it
                if self.energized:
                    self.energized = False
                    self.timeCoilCycle = currentTime

                #if the valve is being closed already, continue closing it, but check if it has closed fully.
                else:
                    if currentTime - self.timeCoilCycle > self.closeDelay
                    self.open = False
                    self.timeValveCycled = currentTime