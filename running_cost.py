# running cost evaluation depends on fuel consumption, and generation patterns
from pylab import *
import numpy as np

class runningCost(object):

    @staticmethod
    def basicCalc(data_list):
    # this method calculates variables used throughout the class
        # time list
        global t
        t = data_list[0].timeList

        # 2D list of total fuel consumption per system
        global fuel_list
        fuel_list = np.array([[0.0]*len(t) for i in range(len(data_list))])

        for i in range(len(data_list)):
            # temp variable to calculate total fuel (diesel and gas) consumed by one controller
            temp_fuel = np.array([0.0] * len(t))
            data = data_list[i]

            for j in range(data.nDer):
                if (data.derList[j].energy_type == ('Diesel' or 'Gas')):
                    temp_fuel += np.array(data.derList[j].consumption)

            fuel_list[i] = temp_fuel

        # note: emissions are linked to fuel consumption. If emissions data is given, then add another variable/metric

    @staticmethod
    # plot power generation over time
    def pwrGen(data_list, canvas):
        for i in range(len(fuel_list)):
            if np.all(fuel_list[i] == 0):
                canvas.axes.plot(t, [] * len(t), label=data_list[i].controllerName)
            elif not np.all(fuel_list[i] == 0):
                canvas.axes.plot(t, fuel_list[i], label=data_list[i].controllerName)

        # total generation capacity for each fuel type
        # note the capacity is a SYSTEM property, indep. of controller; calculate only once
        data = data_list[0]
        fuel_cap = 0
        for i in range(0, data.nDer):
            if (data.derList[i].energy_type == ('Diesel' or 'Gas')):
                fuel_cap += data.derList[i].capacity

        # add generation threshold plot to graph
        canvas.axes.plot(t, [fuel_cap/2]*len(t), 'r--', label='Gen. Threshold (50% cap)')
        # todo: add user input/data input to decide what % of capacity the threshold should be, to max efficiency

        canvas.axes.legend(loc='lower left', fontsize=7)
        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('Power Generation (MW)')
        canvas.axes.set_title('Time Plot of Total Power Gen. (Diesel & Gas)')

    @staticmethod
    def ramping(data_list):
    # use d(P_gen)/dt vs t to show ramping
        fuel_diff = np.array([[0.0]*len(t) for i in range(len(data_list))])
        for i in range(len(fuel_list)):
            fuel_diff[i] = np.gradient(fuel_list[i])

        # total slope of power gen. over time per controller
        global total_grad
        total_grad = [0]*len(data_list)
        for i in range(len(data_list)):
            for j in range(len(t)):
                total_grad[i] += abs(fuel_diff[i][j])

        # max. slope of power gen. over time per controller
        global max_ramping
        max_ramping = [0]*len(data_list)
        for i in range(len(data_list)):
            for j in range(len(t)):
                if abs(fuel_diff[i][j] > max_ramping[i]):
                    max_ramping[i] = abs(fuel_diff[i][j])

    @staticmethod
    def rcStats(data_list):
    # this method calculates various statistics for displaying in a table in the GUI

        # 2D list for storing statistics for each controller
        stats = [[0]*5 for i in range(len(data_list))]

        # total fuel consumption per controller
        for i in range(len(data_list)):
            stats[i][0] = '%.2f' % np.sum(fuel_list[i])

        # total on/off switching (per source) per controller
        for i in range(len(data_list)):
            switching = 0
            for j in range(data_list[0].nDer):
                for k in range(len(t)-1):
                    if ((data_list[i].derList[j].output[k] != 0) and (data_list[i].derList[j].output[k+1] == 0)):
                        switching += 1
            stats[i][1] = switching

        # ramping info
        avg_grad = [int(x/len(t)) for x in total_grad]     # normalized
        for i in range(len(data_list)):
            stats[i][2] = avg_grad[i]
            stats[i][3] = '%.1f' % max_ramping[i]

        # peak demand per controller
        for a in range(len(data_list)):
            peak_pwr = 0.0
            for i in range(data_list[0].nLoad):
                if data_list[a].loadList[i].load_type != 'Dump':
                    for j in range(len(t)):
                        if (data_list[a].loadList[i].demand[j] > peak_pwr):
                            peak_pwr = data_list[a].loadList[i].demand[j]
            stats[a][4] = '%.2f' % peak_pwr

        return stats