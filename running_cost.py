# running cost evaluation depends on fuel consumption and generation patterns
# **assume all possible DER types are Fuel (Diesel, Gas, Propane...), Renewable (Wind, Hydro, PV...), and Storage **
from pylab import *
import numpy as np


class RunningCost(object):

    """ This method calculates variables used throughout the class"""
    @staticmethod
    def basic_calc(data_list):
        # time list
        global t
        t = data_list[0].timeList

        # list of fuel types
        global fuel_types

        # number of fuel types, int
        global num_fuel

        fuel_types = []
        for i in range(data_list[0].nDer):
            if 'Fuel' in data_list[0].derList[i].energy_type:
                fuel_types.append(data_list[0].derList[i].energy_type)

        fuel_types = list(set(fuel_types))
        num_fuel = len(fuel_types)

        # 3D list of fuel consumption per type per sample
        global fuels

        # list of total generation capacity for each fuel type
        # note the capacity is a SYSTEM property, indep. of controller
        global cap_list

        fuels = np.array([[[0.0]*len(t) for j in range(num_fuel)] for i in range(len(data_list))])
        cap_list = [0.0]*num_fuel

        for i in range(len(data_list)):
            for j in range(num_fuel):
                # temp variable to hold total fuel of one type consumed in a sample
                temp_fuel = np.array([0.0]*len(t))
                for x in range(data_list[i].nDer):
                    if data_list[i].derList[x].energy_type == fuel_types[j]:
                        temp_fuel += np.array(data_list[i].derList[x].consumption)
                        if i == 0:
                            cap_list[j] += np.array(data_list[i].derList[x].capacity)
                            # only needs to be calculated once
                fuels[i][j] = temp_fuel

        # 2D list of total fuel consumption per sample
        global total_fuel_list
        total_fuel_list = np.array([[0.0]*len(t) for i in range(len(data_list))])
        for i in range(len(data_list)):
            for j in range(num_fuel):
                total_fuel_list[i] += fuels[i][j]

        # 3D list of power generation from non-renewables per type per sample
        global fuel_gen
        fuel_gen = np.array([[[0.0]*len(t) for j in range(num_fuel)] for i in range(len(data_list))])
        for i in range(len(data_list)):
            for j in range(num_fuel):
                # temp variable to hold total generation by one type of fuel in a sample
                temp_gen = np.array([0.0]*len(t))
                for x in range(data_list[i].nDer):
                    if data_list[i].derList[x].energy_type == fuel_types[j]:
                        temp_gen += np.array(data_list[i].derList[x].output)
                fuel_gen[i][j] = temp_gen

        # 2D list of total fuel generation per sample
        global total_gen_list
        total_gen_list = np.array([[0.0] * len(t) for i in range(len(data_list))])
        for i in range(len(data_list)):
            for j in range(num_fuel):
                total_gen_list[i] += fuel_gen[i][j]

        return fuel_types

        # note: emissions are linked to fuel consumption. If emissions data is given, then add another variable/metric

    """ This method plots (fuel) power generation over time"""
    @staticmethod
    def pwrGen(data_list, ftype, canvas):

        # each fuel type has a different line style
        line_styles = ['--', '-.', '_', ':']
        # ^ assumes max 4 fuel types
        if len(line_styles) < num_fuel:
            line_styles.extend(line_styles)

        # each controller has one colour for all its plots
        colours = ['b', 'g', 'm', 'y', 'c', 'deepskyblue', 'limegreen', 'blueviolet']
        # ^ assumes max 8 controllers being compared at a time

        # plot total generation, or...
        for i in range(len(data_list)):
            if ftype == 0:
                canvas.axes.plot(t, total_gen_list[i], linewidth=2, linestyle=None, color=colours[i],
                                 label=(data_list[i].controllerName + ': Total Fuel Consumption'))
            # ...plot one type of fuel generation and the capacity for that fuel type
            else:
                canvas.axes.plot(t, fuel_gen[i][ftype-1], linestyle=line_styles[ftype-1], color=colours[i],
                                 label=(data_list[i].controllerName + ': ' + fuel_types[ftype-1][5:]))
        if ftype != 0:
            canvas.axes.plot(t, [cap_list[ftype-1]*0.3]*len(t), linestyle=line_styles[ftype-1], color='red',
                             label='Gen. Threshold (30% cap)')

        # todo: add user input/data input to decide what % of capacity the threshold should be, to max efficiency

        canvas.axes.legend(loc='upper right', fontsize=7)
        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('Power Generation (MW)')
        canvas.axes.set_title('Time Plot of Fuel-Powered Generation')

    """ Plot (fuel consumption/power out) vs power out to find most efficient operating point in terms of fuel use"""
    @staticmethod
    def fuelUse(data_list, ftype, canvas):
        # power out needs to match fuel consumption: ie per source per sample
        # y is a 3D array of fuel use/ pwr out
        y = np.array([[[0.0]*len(t) for j in range(num_fuel)] for i in range(len(data_list))])
        for i in range(len(data_list)):
            for j in range(num_fuel):
                for k in range(len(t)):
                    if fuel_gen[i][j][k] != 0:
                        y[i][j][k] = float((fuels[i][j][k]/fuel_gen[i][j][k]))
                    else:
                        y[i][j][k] = 0

        # total (fuel consumption/power output)
        y_tot = np.array([[0.0]*len(t) for i in range(len(data_list))])
        for i in range(len(data_list)):
            for j in range(num_fuel):
                y_tot[i] += y[i][j]

        colours = ['b', 'g', 'm', 'y', 'c', 'deepskyblue', 'limegreen', 'blueviolet']

        if ftype == 0:
            for i in range(len(data_list)):
                canvas.axes.scatter(total_gen_list[i], y_tot[i], color=colours[i], s=15,
                                    label=(data_list[i].controllerName + ': Total Fuel'))
        else:
            for i in range(len(data_list)):
                # add min point recognition to plot
                y_min = min(y[i][ftype - 1])
                x_min = [fuel_gen[i][ftype - 1][np.where(y[i][ftype-1] == y_min)]]
                min_fuel = fuels[i][ftype - 1][np.where(y[i][ftype-1] == y_min)]

                canvas.axes.scatter(fuel_gen[i][ftype-1], y[i][ftype-1], color=colours[i], s=15,
                                    label=(fuel_types[ftype-1][5:] + ' efficient fuel level: %s L' % min_fuel))
                canvas.axes.plot(x_min, y_min, '-rx')

        canvas.axes.legend(loc='upper right', fontsize=7)
        canvas.axes.set_xlabel('Power Output')
        canvas.axes.set_ylabel('Fuel Consumption/Power Output')
        canvas.axes.set_title('Fuel Consumption/Power Output vs. Power Output')

    @staticmethod
    def ramping(data_list):
        # use d(P_gen)/dt vs t (gradient) to show ramping
        fuel_diff = np.array([[0.0]*len(t) for i in range(len(data_list))])
        for i in range(len(data_list)):
            fuel_diff[i] = np.gradient(total_gen_list[i])

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

    """ This method provides data for a table to give info on switching. Info is per generator (DER).
    (Inefficient generation (below 30% capacity) is indicated in the power_out vs time plot)"""
    @staticmethod
    def switching(data_list):
        # 2D list: No. of switches per DER per sample
        switch_list = [[0]*data_list[0].nDer for i in range(len(data_list))]

        for i in range(len(data_list)):
            for j in range(data_list[0].nDer):
                switching = 0
                if 'Fuel' in data_list[i].derList[j].energy_type:
                    # for fuel generation, 'off' is when consumption = 0
                    for k in range(len(t) - 1):
                        if (data_list[i].derList[j].consumption[k] != 0) and (data_list[i].derList[j].consumption[k + 1] == 0):
                            switching += 1
                elif 'Ren' in data_list[i].derList[j].energy_type:
                    # for renewable generation, 'off' is when generation is < 5% capacity
                    for k in range(len(t) - 1):
                        cap = data_list[i].derList[j].capacity
                        if (data_list[i].derList[j].output[k] > cap*0.05) and (data_list[i].derList[j].output[k + 1] < cap*0.05):
                            switching += 1
                switch_list[i][j] = switching

        return switch_list

    """ This method calculates various statistics for displaying in a table in the GUI"""
    @staticmethod
    def rcStats(data_list):
        # 2D list for storing statistics for each controller
        stats = [[] for i in range(len(data_list))]

        # total fuel consumption per controller
        for i in range(len(data_list)):
            stats[i].append('%.2f' % np.sum(total_fuel_list[i]))

        # ramping info
        avg_grad = [int(x/len(t)) for x in total_grad]     # normalized
        for i in range(len(data_list)):
            stats[i].append(avg_grad[i])
            stats[i].append('%.1f' % max_ramping[i])

        # peak demand per controller
        for a in range(len(data_list)):
            peak_pwr = 0.0
            for i in range(data_list[0].nLoad):
                if data_list[a].loadList[i].load_type != 'Dump':
                    for j in range(len(t)):
                        if data_list[a].loadList[i].demand[j] > peak_pwr:
                            peak_pwr = data_list[a].loadList[i].demand[j]
            stats[a].append('%.2f' % peak_pwr)
        return stats
