from pylab import *
import matplotlib.pyplot as plt
from running_cost import *
from data import *


Data1 = [Data('sample1.txt')]
Data2 = [Data('sample1.txt'), Data('sample2.txt')]
print("got data")
RunningCost.basicCalc(Data1)
#runningCost.basicCalc(Data2)
RunningCost.fuelUse(Data1)
#runningCost.fuelUse(Data2)
print('basic calc done')

