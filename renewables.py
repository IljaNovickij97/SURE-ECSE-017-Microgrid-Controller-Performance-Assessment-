import numpy as np
from pylab import *
import matplotlib.pyplot as plt

import data
# **assume all possible DER types are Deisel, Gas, Wind, Hydro, PV**

class renewables(object):
    Data = data.Data('sample.txt')

    @staticmethod
    def renewablePie(data, canvas):

        genList = [None]*data.nDer
        for i in range (0, data.nDer):
            #total generation per source
            genList[i] = sum(data.derList[i].output)
        typeList = [None]*data.nDer
        for i in range (0, data.nDer):
            typeList[i] = data.derList[i].energy_type

        #pie chart:
        figure(1, figsize=(6, 6))   #this and the following line are copied from online, idk what they're for excactly, something to do with making the canvas
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
        colors = ['magenta', 'lightskyblue', 'gold', 'yellowgreen', 'lightcoral']
        explode = (0, 0, 0.05, 0.05, 0.05)
        canvas.axes.title('Pie chart showing total power generation and proportion of renewables')
        canvas.axes.pie(fracs, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)

    @staticmethod
    def renewableTime(data, canvas):
        t = data.timeList
        wind, hydro, pv = ([] for i in range(3))
        for i in range(0, data.nDer):
            if data.derList[i].type == 'Wind':
                wind += data.derList[i].output
            if data.derList[i].type == 'Hydro':
                hydro += data.derList[i].output
            if data.derList[i].type == 'PV':
                pv += data.derList[i].output

        total = wind + hydro + pv

        canvas.axes.plot(t, wind, label="Wind Gen")
        canvas.axes.plot(t, hydro, label="Hydro Gen")
        canvas.axes.plot(t, pv, label="Solar Gen")
        canvas.axes.plot(t, total, label="Total Renewable Gen")
        canvas.axes.legend(loc='upper left')
        canvas.axes.xlabel('Time')
        canvas.axes.ylabel('Power Generation')
        canvas.axes.title('Time plot showing renewable power generation over entire sample')

