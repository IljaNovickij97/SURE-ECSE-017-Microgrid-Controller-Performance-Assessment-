# running cost evaluation depends on fuel consumption, and generation patterns
from pylab import *
import numpy as np

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
            if data.derList[i].energy_type == 'Diesel':
                diesel += np.array(data.derList[i].consumption)
            if data.derList[i].energy_type == 'Gas':
                gas += np.array(data.derList[i].consumption)

        global total_fuel
        total_fuel = gas + diesel
    # note: emissions are linked to fuel consumption. If emissions data is given, then add another calculation

    @staticmethod
    # plot power generation over time
    def pwrGen(data, canvas):
        if np.all(total_fuel == 0):
            canvas.axes.plot(t, [] * len(t), label="Total Fuel Gen")
        elif not np.all(total_fuel == 0):
            canvas.axes.plot(t, total_fuel, label="Total Fuel Gen")

        # total generation capacity for each fuel type
        diesel_cap, gas_cap = 0, 0
        for i in range(0, data.nDer):
            if (data.derList[i].energy_type == 'Diesel'):
                diesel_cap += data.derList[i].capacity
            if (data.derList[i].energy_type == 'Gas'):
                gas_cap += data.derList[i].capacity
        total_cap = diesel_cap + gas_cap
        canvas.axes.plot(t, [total_cap/2]*len(t), label='Gen. Threshold')
        canvas.axes.legend(loc='upper left')
        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('Power Generation (MW)')
        canvas.axes.set_title('Time Plot of Non-Renewable Power Gen.')  # todo: change to show controller name

    @staticmethod
    # plot d(P_gen)/dt vs t to show ramping
    def ramping(data, canvas):
        fuel_diff = np.gradient(total_fuel)
        if np.all(fuel_diff == 0):
            canvas.axes.plot(t, []*len(t))
        elif not np.all(fuel_diff == 0):
            canvas.axes.plot(t, fuel_diff)
        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('d(P_Gen)/dt')
        canvas.axes.set_title('Power Gen. Ramping')

        # calculate total slope (point-wise dP/dt):
        # greater slope indicates more ramping
        global total_grad
        total_grad = 0
        for i in range (0, len(t)):
            total_grad += abs(fuel_diff[i])

    @staticmethod
    def rcStats(data):
        consumption = [sum(diesel), sum(gas), (sum(diesel)+sum(gas))]

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
        return stats