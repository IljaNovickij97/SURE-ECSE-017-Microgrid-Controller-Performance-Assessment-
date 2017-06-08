# running cost evaluation depends on fuel consumption, and generation patterns
# **assume all possible DER types are Fuel (Diesel, Gas, Propane...), Renewable (Wind, Hydro, PV...), and Storage **
from pylab import *
import numpy as np
from itertools import cycle

class runningCost(object):

    @staticmethod
    def basicCalc(data_list):
    # this method calculates variables used throughout the class
        # time list
        global t
        t = data_list[0].timeList

        # 3D list of fuel consumption per type per sample
        global fuels

        # list of fuel types
        global fuel_type

        # list of total generation capacity for each fuel type
        # note the capacity is a SYSTEM property, indep. of controller
        global cap_list

        # number of fuel types, int
        global num_fuel

        fuel_type = []
        for i in range(data_list[0].nDer):
            if 'Fuel' in data_list[0].derList[i].energy_type:
               fuel_type.append(data_list[0].derList[i].energy_type)

        fuel_type = list(set(fuel_type))
        num_fuel = len(fuel_type)
        print(fuel_type)

        fuels = np.array([[[0.0]*len(t) for j in range(num_fuel)] for i in range(len(data_list))])
        cap_list = [0.0]*(num_fuel)

        for i in range(len(data_list)):
            for j in range(num_fuel):
                # temp variable to hold total fuel of one type consumed in a sample
                temp_fuel = np.array([0.0]*len(t))
                for x in range(data_list[i].nDer):
                    if data_list[i].derList[x].energy_type == fuel_type[j]:
                        temp_fuel += np.array(data_list[i].derList[x].consumption)
                        if i == 0:
                            cap_list[j] += np.array(data_list[i].derList[x].capacity)
                            # only needs to be calculated once
                fuels[i][j] = temp_fuel
        print("fuels: ",fuels)

        # 2D list of total fuel consumption per sample
        global total_fuel_list
        total_fuel_list = np.array([[0.0]*len(t) for i in range(len(data_list))])
        for i in range(len(data_list)):
            for j in range(num_fuel):
                total_fuel_list[i] += fuels[i][j]
        print("total fuel list: ", total_fuel_list)

        # 3D list of power generation from non-renewables per type per sample
        global fuel_gen
        fuel_gen = ([[[0.0]*len(t) for j in range(num_fuel)] for i in range(len(data_list))])
        for i in range(len(data_list)):
            for j in range(num_fuel):
                # temp variable to hold total generation by one type of fuel in a sample
                temp_gen = np.array([0.0]*len(t))
                for x in range(data_list[i].nDer):
                    if data_list[i].derList[x].energy_type == fuel_type[j]:
                        temp_gen += np.array(data_list[i].derList[x].output)
                fuel_gen[i][j] = temp_gen
        print("fuel gen: ", fuel_gen)

        # note: emissions are linked to fuel consumption. If emissions data is given, then add another variable/metric

    @staticmethod
    # todo: to rotate between fuel type plots...find a way of separating fuel type plots...
    # plot power generation over time
    def pwrGen(data_list, canvas):
        print("pwrGen")
        line_styles = ['-', '--', '-.', '_', ':']
        if (len(line_styles) < num_fuel):
            line_styles.extend(line_styles)
        colors = ['b', 'g', 'm', 'y', 'c', 'deepskyblue', 'limegreen', 'blueviolet']
        for i in range(len(data_list)):
            if np.all(total_fuel_list[i] == 0):
                canvas.axes.plot(t, [0]*len(t), linewidth=4, linestyle=None, color=colors[i],
                                 label=(data_list[i].controllerName, 'Total Fuel Consumption'))
            elif not np.all(total_fuel_list[i] == 0):
                canvas.axes.plot(t, total_fuel_list[i], linewidth=4, linestyle=None, color=colors[i],
                                 label=(data_list[i].controllerName, 'Total Fuel Consumption'))
            for j in range(num_fuel):
                if np.all(fuels[i][j] == 0):
                    canvas.axes.plot(t, [0]*len(t), linestyle=line_styles[j], color=colors[i], label=fuel_type[j])
                elif not np.all(fuels[i][j] == 0):
                    canvas.axes.plot(t, fuels[i][j], linestyle=line_styles[j], color=colors[i], label=fuel_type[j])

        # add generation threshold plot to graph
        print(num_fuel)
        print(cap_list)
        for i in range(num_fuel):
            canvas.axes.plot(t, [cap_list[i]*0.3]*len(t), linestyle=line_styles[i], color='red', label='Gen. Threshold (30% cap)')
        # todo: add user input/data input to decide what % of capacity the threshold should be, to max efficiency

        canvas.axes.legend(loc='lower left', fontsize=7)
        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('Power Generation (MW)')
        canvas.axes.set_title('Time Plot of Power Gen. with Fuel')


    @staticmethod
    # plot (fuel consumption/power out) vs power out to find most efficient operating point (in terms of fuel use)
    def fuelUse(data_list, canvas):
        print("Fuel Use")
        # power out needs to match fuel consumption: ie per source per sample
        y = [[[0.0]*len(t) for j in range(num_fuel)] for i in range(len(data_list))]
        for i in range(len(data_list)):
            for j in range(num_fuel):
                for k in range(len(t)):
                    if fuel_gen[i][j][k] != 0:
                        y[i][j][k] = (fuels[i][j][k]/fuel_gen[i][j][k])
                    else:
                        y[i][j][k] = max(fuel_gen[i][j])
                y[i][j].sort()
                fuel_gen[i][j].sort()

        line_styles = ['-', '--', '-.', '_', ':']
        colors = ['b', 'g', 'm', 'y', 'c', 'deepskyblue', 'limegreen', 'blueviolet']
        if (len(line_styles) < num_fuel):
            line_styles.extend(line_styles)
        for i in range(len(data_list)):
            for j in range(num_fuel):
                if np.all(fuel_gen[i][j] == 0):
                    canvas.axes.plot(y[i][j], [0]*len(t), linestyle=line_styles[j], color=colors[i], label=fuel_type[j])
                elif not np.all(fuels[i][j] == 0):
                    canvas.axes.plot(y[i][j], fuel_gen[i][j], linestyle=line_styles[j], color=colors[i], label=fuel_type[j])

        canvas.axes.legend(loc='lower left', fontsize=7)
        canvas.axes.set_xlabel('Power Output')
        canvas.axes.set_ylabel('Fuel Consumption/Power Output')
        canvas.axes.set_title('Plot to find most efficient operating point (in terms of fuel use)')

    # @staticmethod
    # def ramping(data_list):
    # # use d(P_gen)/dt vs t to show ramping
    #     fuel_diff = np.array([[0.0]*len(t) for i in range(len(data_list))])
    #     for i in range(len(power_gen)):
    #         fuel_diff[i] = np.gradient(power_gen[i])
    #
    #     # total slope of power gen. over time per controller
    #     global total_grad
    #     total_grad = [0]*len(data_list)
    #     for i in range(len(data_list)):
    #         for j in range(len(t)):
    #             total_grad[i] += abs(fuel_diff[i][j])
    #
    #     # max. slope of power gen. over time per controller
    #     global max_ramping
    #     max_ramping = [0]*len(data_list)
    #     for i in range(len(data_list)):
    #         for j in range(len(t)):
    #             if abs(fuel_diff[i][j] > max_ramping[i]):
    #                 max_ramping[i] = abs(fuel_diff[i][j])

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