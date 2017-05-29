from pylab import *
import data
# **assume all possible DER types are Diesel, Gas, Wind, Hydro, PV!**

class Renewables(object):
    Data = data.Data('sample.txt')

    @staticmethod
    # pie chart showing % renewable generation of total power out
    def renewablePie(data, canvas):

        genList = [None]*data.nDer
        # total generation per source
        for i in range (0, data.nDer):
            genList[i] = sum(data.derList[i].output)
        typeList = [None]*data.nDer
        # lists type of each 'n' sources
        for i in range (0, data.nDer):
            typeList[i] = data.derList[i].energy_type

        #pie chart:
        labels = 'Diesel', 'Gas', 'Wind', 'Hydro', 'PV'
        # array to be used for chart
        chartList = np.array([0]*5)
        for i in range (0, data.nDer):
            if typeList[i] == 'Diesel\n':
                chartList[0] += genList[i]
            elif typeList[i] == 'Gas\n':
                chartList[1] += genList[i]
            elif typeList[i] == 'Wind\n':
                chartList[2] += genList[i]
            elif typeList[i] == 'Hydro\n':
                chartList[3] += genList[i]
            elif typeList[i] == 'PV\n':
                chartList[4] += genList[i]

        colors = ['magenta', 'lightskyblue', 'gold', 'yellowgreen', 'lightcoral']
        explode = (0, 0, 0.07, 0.07, 0.07)
        canvas.axes.set_title('Pie chart of Total Power Gen. & Percentage Renewables')
        canvas.axes.pie(chartList, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        #add border lines if possible

    @staticmethod
    # plot of renewable power generation levels over time
    def renewableTime(data, canvas):
    # todo: fix timescale to match units
    # todo: adjust power units
        t = data.timeList
        wind = np.array([0.0]*len(data.timeList))
        hydro = np.array([0.0]*len(data.timeList))
        pv = np.array([0.0]*len(data.timeList))

        for i in range(0, data.nDer):
            if data.derList[i].energy_type == 'Wind\n':
                wind += np.array(data.derList[i].output)
            if data.derList[i].energy_type == 'Hydro\n':
                hydro += np.array(data.derList[i].output)
            if data.derList[i].energy_type == 'PV\n':
                pv += np.array(data.derList[i].output)

        total = wind + hydro + pv

        if not np.all(wind==0):
            canvas.axes.plot(t, wind, label="Wind Gen")
        if not np.all(hydro==0):
            canvas.axes.plot(t, hydro, label="Hydro Gen")
        if not np.all(pv==0):
            canvas.axes.plot(t, pv, label="Solar Gen")
        if np.all(total==0):
            canvas.axes.plot(t, []*len(data.timeList), label="Total Renewable Gen")
        elif not np.all(total==0):
            canvas.axes.plot(t, total, label="Total Renewable Gen")
        canvas.axes.legend(loc='upper left')
        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('Power Generation (MW)')
        canvas.axes.set_title('Time Plot of Renewable Power Gen.')

