# running cost evaluation depends on fuel consumption, and generation patterns
from pylab import *
import numpy as np
import data

class runningCost(object):
    t, diesel, gas = [], [], []

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
                gas += np.array(data.derList[i].consumption)

        global total_fuel
        total_fuel = gas + diesel
    # note: emissions are linked to fuel consumption. If emissions data is given, then add another calculation

    @staticmethod
    # plot power generation over time
    def pwrGen(data, canvas):
        if not np.all(diesel == 0):
            canvas.axes.plot(t, diesel, label="Diesel Gen")
        if not np.all(gas == 0):
            canvas.axes.plot(t, gas, label="Gas Gen")
        if np.all(total_fuel == 0):
            canvas.axes.plot(t, [] * len(data.timeList), label="Total Non-Renewable Gen")
        elif not np.all(total_fuel == 0):
            canvas.axes.plot(t, total_fuel, label="Total Non-Renewable Gen")

        # total generation capacity for each fuel type
        diesel_cap, gas_cap = 0
        for i in range(0, data.nDer):
            if data.derList[i].energy_type == 'Diesel':
                diesel_cap += data.derList[i].capacity
            if data.derList[i].energy_type == 'Gas':
                gas_cap += data.derList[i].capacity

        print (gas_cap)

        canvas.axes.plot(t, diesel_cap/2, label='Diesel Gen. Threshold')
        canvas.axes.plot(t, gas_cap/2, label='Gas Gen. Threshold')

        canvas.axes.legend(loc='upper left')
        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('Power Generation (MW)')
        canvas.axes.set_title('Time Plot of Non-Renewable Power Gen.')
        canvas.draw()

    @staticmethod
    # plot d(P_gen)/dt vs t to show ramping
    def ramping(data, canvas):
        fuel_diff = np.diff(total_fuel, n=1, axis=t)
        if np.all(fuel_diff == 0):
            canvas.axes.plot(t, [] * len(t))
        elif not np.all(fuel_diff == 0):
            canvas.axes.plot(t, fuel_diff)

        print(fuel_diff)

        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('d(P_Gen)/dt')
        canvas.axes.set_title('Power Gen. Derivative vs Time, showing Ramping')
        canvas.draw()

        # calculate total slope (point-wise dP/dt):
        # greater slope indicates more ramping
        global total_grad
        total_grad = 0
        for i in range (0, len(t)):
            total_grad += abs(fuel_diff[i])

        print(total_grad)

    @staticmethod
    def rcStats(data):
        consumption = [sum(diesel), sum(gas), (sum(diesel)+sum(gas))]
        total_grad = 5768

        # calculate total on/off switching (per source)
        switching = 0
        for i in range(0, data.nDer):
            for j in range (0, len(t)-1):
                if ((data.derList[i].output[j] != 0) and (data.derList[i].output[j+1] == 0)):
                    switching += 1

        # find peak demand
        peak_pwr = 0
        for i in range(0, data.nLoad):
            if data.loadList[i].load_type != 'Dump':
                for j in range(0, len(t)):
                    if (data.loadList[i].demand[j] > peak_pwr):
                        peak_pwr = data.loadList[i].demand[j]

        stats = [consumption, switching, (total_grad/len(t)), peak_pwr]
        print(consumption)
        print(switching)
        print(peak_pwr)
        return stats

Data = data.Data('renewable_ex.txt')
runningCost.basicCalc(Data)
runningCost.rcStats(Data)