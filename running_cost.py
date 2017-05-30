# running cost evaluation depends on unit commitment and generator output
# unit commitment = total time for P_dem =/= 0
from pylab import *
import numpy as np

class runningCost(object):
    t = []
    diesel = []
    gas = []

    # def __init__(self):
    #     # Put stuff here if using variables throughout the class i.e. something that's calculated for all of the methods
    #     # below
    #     pass

    @staticmethod
    def basicCalc(data):
        global t
        t = data.timeList
        global diesel
        diesel = np.array([0.0] * len(t))
        global gas
        gas = np.array([0.0] * len(t))

        for i in range(0, data.nDer):
            if data.derList[i].energy_type == 'Diesel\n':
                diesel += np.array(data.derList[i].consumption)
            if data.derList[i].energy_type == 'Gas\n':
                gas += np.array(data.derList[i].cosumption)

        global totalFuel
        totalFuel = gas + diesel

    @staticmethod
    # plot power generation over time
    def pwrGen(data, canvas):
        if not np.all(diesel == 0):
            canvas.axes.plot(t, diesel, label="Diesel Gen")
        if not np.all(gas == 0):
            canvas.axes.plot(t, gas, label="Gas Gen")
        if np.all(totalFuel == 0):
            canvas.axes.plot(t, [] * len(data.timeList), label="Total Non-Renewable Gen")
        elif not np.all(totalFuel == 0):
            canvas.axes.plot(t, totalFuel, label="Total Non-Renewable Gen")

        diesel_cap, gas_cap = 0
        for i in range(0, data.nDer):
            if data.derList[i].energy_type == 'Diesel\n':
                diesel_cap += data.derList[i].capacity
            if data.derList[i].energy_type == 'Gas\n':
                gas_cap += data.derList[i].capacity

        # calculate total on/off switching (where off is considered to be less than 50% of generation capacity)
        global diesel_switch
        global gas_switch
        for i in range (0, t-1):
            if (diesel[i] > diesel_cap) and (diesel[i+1] < diesel_cap):
                diesel_switch += 1
            if (gas[i] > gas_cap) and (gas[i+1] < gas_cap):
                gas_switch += 1

        canvas.axes.plot(t, diesel_cap/2, label='Deisel Gen. Threshold')
        canvas.axes.plot(t, gas_cap/2, label='Gas Gen. Threshold')

        canvas.axes.legend(loc='upper left')
        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('Power Generation (MW)')
        canvas.axes.set_title('Time Plot of Non-Renewable Power Gen.')
        canvas.draw()

    @staticmethod
    # plot d(P_gen)/dt vs t to show ramping
    def ramping(data, canvas):
        fuelDiff = np.diff(totalFuel, n=1, axis=t)
        if np.all(fuelDiff == 0):
            canvas.axes.plot(t, [] * len(data.timeList))
        elif not np.all(fuelDiff == 0):
            canvas.axes.plot(t, fuelDiff)

        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('d(P_Gen)/dt')
        canvas.axes.set_title('Power Gen. Derivative vs Time, showing Ramping')
        canvas.draw()

    @staticmethod
    def rc_stats():
        consumption = [sum(diesel), sum(gas), (sum(diesel)+sum(gas))]
        switching = [diesel_switch, gas_switch]
        stats = [consumption, switching]
        return stats
