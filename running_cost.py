# running cost evaluation depends on unit commitment and generator output
# unit commitment = total time for P_dem =/= 0
from pylab import *
import data

class runningCost(object):
    def __init__(self):
        # Put stuff here if using variables throughout the class i.e. something that's calculated for all of the methods
        # below
        pass

    @staticmethod
    def fuelConsumption(data, canvas):      #plot of fuel consumption over time
        t = data.timeList
        diesel = np.array([0.0]*len(t))
        gas = np.array([0.0] * len(t))

        for i in range(0, data.nDer):
            if data.derList[i].energy_type == 'Diesel\n':
                diesel += np.array(data.derList[i].consumption)
            if data.derList[i].energy_type == 'Gas\n':
               gas += np.array(data.derList[i].cosumption)

        total = gas + diesel

        if not np.all(diesel==0):
            canvas.axes.plot(t, diesel, label="Diesel Consumption")
        if not np.all(gas==0):
            canvas.axes.plot(t, gas, label="Gas Consumption")
        if np.all(total==0):
            canvas.axes.plot(t, []*len(data.timeList), label="Total Fuel Consumption")
        elif not np.all(total==0):
            canvas.axes.plot(t, total, label="Total Fuel Consumption")
        canvas.axes.legend(loc='upper left')
        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('Fuel Consumption (Litres)')
        canvas.axes.set_title('Time Plot Fossil Fuel Consumption')

    @staticmethod
    def pwrGen(data, canvas):
        t = data.timeList
        diesel = np.array([0.0] * len(data.timeList))
        gas = np.array([0.0] * len(data.timeList))

        for i in range(0, data.nDer):
            if data.derList[i].energy_type == 'Diesel\n':
                diesel += np.array(data.derList[i].output)
            if data.derList[i].energy_type == 'Gas\n':
                gas += np.array(data.derList[i].output)

        total = gas + diesel

        if not np.all(diesel == 0):
            canvas.axes.plot(t, diesel, label="Diesel Gen")
        if not np.all(gas == 0):
            canvas.axes.plot(t, gas, label="Gas Gen")
        if np.all(total == 0):
            canvas.axes.plot(t, [] * len(data.timeList), label="Total Non-Renewable Gen")
        elif not np.all(total == 0):
            canvas.axes.plot(t, total, label="Total Non-Renewable Gen")
        canvas.axes.legend(loc='upper left')
        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('Power Generation (MW)')
        canvas.axes.set_title('Time Plot of Non-Renewable Power Gen.')

    @staticmethod
    def consumptionStats(data):
        stats = [None]*3
        t = data.timeList
        diesel = np.array([0.0] * len(t))
        gas = np.array([0.0] * len(t))

        for i in range(0, data.nDer):
            if data.derList[i].energy_type == 'Diesel\n':
                diesel += np.array(data.derList[i].consumption)
            if data.derList[i].energy_type == 'Gas\n':
                gas += np.array(data.derList[i].cosumption)

        stats[0] = sum(diesel)     # total Diesel consumption
        stats[1] = sum(gas)        # total gas consumption
        stats[2] = sum(diesel) + sum(gas)   # total fuel consumption

