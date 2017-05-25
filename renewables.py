import numpy as np
from pylab import *

class renewables(object):
    def __init__(self):
        # Put stuff here if using variables throughout the class i.e. something that's calculated for all of the methods
        # below
        pass

    @staticmethod
    def renewableGen(data, canvas):
        # assume all possible DER types are Deisel, Gas, Wind, Hydro, PV
        genList = [None]*data.nDer
        for i in range (0, data.nDer):
            #total generation per source
            genList[i] = sum(data.derList[i].output)
        typeList = [None]*data.nDer
        for i in range (0, data.nDer):
            typeList[i] = data.derList[i].energy_type
        isRenewable = False
        if typeList[k] == ("Wind" or "Hydro" or "PV"):
            isRenewable = True

        #pie chart:
        figure(1, figsize=(6, 6))   #this and the following line are copied from online, idk what they're for
        ax = axes([0.1, 0.1, 0.8, 0.8])

        labels = 'Deisel', 'Gas', 'Wind', 'Hydro', 'PV'
        chartList = [None]*5
        for i in range (0, data.nDer):
            if typeList[i] == 'Deisel':
                chartList[0] += genList[i]
            elif typeList[i] == 'Gas':
                chartList[1] += genList[i]
            elif typeList[i] == 'Wind':
                chartList[2] += genList[i]
            elif typeList[i] == 'Hydro':
                chartList[3] += genList[i]
            elif typeList[i] == 'PV':
                chartList[4] += genList[i]

        fracs = chartList/(sum(chartList))*100
        explode = (0, 0, 0.05, 0.05, 0.05)

        canvas.axes.pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)

        # Do calculations here
        #canvas.axes.plot(x,y)
