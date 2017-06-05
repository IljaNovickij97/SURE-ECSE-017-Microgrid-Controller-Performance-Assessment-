from pylab import *
import numpy as np

# **assume all possible DER types are Diesel, Gas, Wind, Hydro, PV, Storage **

class Renewables(object):

    @staticmethod
    def renewablePie(data, canvas):

        gen_list = [None]*data.nDer
        for i in range(0, data.nDer):
            #total generation per source
            gen_list[i] = sum(data.derList[i].output)
        type_list = [None]*data.nDer
        for i in range(0, data.nDer):
            type_list[i] = data.derList[i].energy_type

        #pie chart:
        labels = ['Diesel', 'Gas', 'Wind', 'Hydro', 'PV']
        chart_list = np.array([0]*5)
        for i in range(0, data.nDer):
            if type_list[i] == 'Diesel':
                chart_list[0] += gen_list[i]
            elif type_list[i] == 'Gas':
                chart_list[1] += gen_list[i]
            elif type_list[i] == 'Wind':
                chart_list[2] += gen_list[i]
            elif type_list[i] == 'Hydro':
                chart_list[3] += gen_list[i]
            elif type_list[i] == 'PV':
                chart_list[4] += gen_list[i]

        fracs = chart_list/(sum(chart_list))*100
        colors = ['magenta', 'lightskyblue', 'gold', 'yellowgreen', 'lightcoral']
        explode = [0, 0, 0.1, 0.1, 0.1]
        canvas.axes.set_title(data.controllerName)
        canvas.axes.pie(fracs, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)


        #add border lines if possible

    @staticmethod
    def renewableTime(data, canvas):
    # todo: fix timescale to match units
    #       adjust power units
        t = data.timeList
        wind = np.array([0.0]*len(data.timeList))
        hydro = np.array([0.0]*len(data.timeList))
        pv = np.array([0.0]*len(data.timeList))

        for i in range(0, data.nDer):
            if data.derList[i].energy_type == 'Wind':
                wind += np.array(data.derList[i].output)
            if data.derList[i].energy_type == 'Hydro':
                hydro += np.array(data.derList[i].output)
            if data.derList[i].energy_type == 'PV':
                pv += np.array(data.derList[i].output)

        total = wind + hydro + pv

        if not np.all(wind == 0):
            canvas.axes.plot(t, wind, label="Wind Gen")
        if not np.all(hydro == 0):
            canvas.axes.plot(t, hydro, label="Hydro Gen")
        if not np.all(pv == 0):
            canvas.axes.plot(t, pv, label="Solar Gen")
        if np.all(total == 0):
            canvas.axes.plot(t, []*len(data.timeList), label="Total Renewable Gen")
        elif not np.all(total == 0):
            canvas.axes.plot(t, total, label="Total Renewable Gen")
        canvas.axes.legend(loc='upper left')
        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('Power Generation (MW)')
        canvas.axes.set_title('Time Plot of Renewable Power Gen.')
        canvas.draw()

    @staticmethod
    def renewable_stats(data):
        wind = np.array([0.0] * len(data.timeList))
        hydro = np.array([0.0] * len(data.timeList))
        pv = np.array([0.0] * len(data.timeList))
        diesel = np.array([0.0]*len(data.timeList))
        gas = np.array([0.0]*len(data.timeList))

        for i in range(0, data.nDer):
            if data.derList[i].energy_type == 'Wind':
                wind += np.array(data.derList[i].output)
            elif data.derList[i].energy_type == 'Hydro':
                hydro += np.array(data.derList[i].output)
            elif data.derList[i].energy_type == 'PV':
                pv += np.array(data.derList[i].output)
            elif data.derList[i].energy_type == 'Diesel':
                diesel += np.array(data.derList[i].output)
            elif data.derList[i].energy_type == 'Gas':
                gas += np.array(data.derList[i].output)

        total_wind, total_hydro, total_pv, total_diesel, total_gas = 0, 0, 0, 0, 0

        for i in range(0, data.samplingPeriod):
            total_wind += wind[i]
            total_hydro += hydro[i]
            total_pv += pv[i]
            total_diesel += diesel[i]
            total_gas += gas[i]

        total_wind /= (data.samplingPeriod*60*60)
        total_hydro /= (data.samplingPeriod*60*60)
        total_pv /= (data.samplingPeriod*60*60)
        total_diesel /= (data.samplingPeriod*60*60)
        total_gas /= (data.samplingPeriod*60*60)

        total_renewable = total_wind + total_hydro + total_pv
        total = total_renewable + total_diesel + total_gas

        stats = [total_wind, total_hydro, total_pv, total_diesel, total_gas, total_renewable, total]

        return stats


