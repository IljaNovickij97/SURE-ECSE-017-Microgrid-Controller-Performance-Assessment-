import numpy as np


class VoltageAndFrequency(object):

    @staticmethod
    def voltage_time_plot(data_list, canvas, busNo):

        for i in range(len(data_list)):
            canvas.axes.plot(data_list[i].busList[busNo].voltage_time,
                             data_list[i].busList[busNo].voltage, linewidth=1.0)

        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('Voltage (pu)')

    @staticmethod
    def voltage_hist(data_list, canvas, busNo, step, lower=0.94, middle_left=0.98, middle_right=1.02, upper=1.06):
        bounds = ['<' + str(lower), str(lower) + '-' + str(middle_left), str(middle_left) + '-' + str(middle_right),
                  str(middle_right) + '-' + str(upper), '>' + str(upper)]
        pos = [0.0, 1.0, 2.0, 3.0, 4.0]

        for i in range(len(data_list)):
            voltage_list = data_list[i].busList[busNo].voltage
            for j in range(len(pos)):
                pos[j] += step
            bins = sort_bin(voltage_list, lower, middle_left, middle_right, upper)
            canvas.axes.bar(pos, bins, align='center', width=step, label=data_list[i].controllerName)

        for j in range(len(pos)):
            pos[j] -= i * step / 2.0

        canvas.axes.set_xticklabels(bounds)
        canvas.axes.set_xticks(pos)
        canvas.axes.set_xlabel('Voltage (pu)')
        canvas.axes.set_ylabel('Number of Occurrences')
        canvas.axes.legend(loc='upper right')

    @staticmethod
    def voltage_stats(data, bus_no):
        stats = [np.std(data.busList[bus_no].voltage), np.mean(data.busList[bus_no].voltage)]
        return stats

    @staticmethod
    def frequency_time_plot(data_list, canvas, busNo):

        for i in range(len(data_list)):
            canvas.axes.plot(data_list[i].busList[busNo].frequency_time,
                             data_list[i].busList[busNo].frequency, linewidth=1.0)

        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('Frequency (Hz)')

    @staticmethod
    def frequency_hist(data_list, canvas, bus_no, step, lower=58.5, middle_left=59.5, middle_right=60.5, upper=61.5):

        if data_list[0].busList[bus_no].frequency_unit == 'pu':
            lower, middle_left, middle_right, upper = 0.94, 0.98, 1.02, 1.06
        bounds = ['<' + str(lower), str(lower)+'-'+str(middle_left), str(middle_left)+'-'+str(middle_right),
                  str(middle_right)+'-'+str(upper), '>'+str(upper)]
        pos = [0.0, 1.0, 2.0, 3.0, 4.0]

        for i in range(len(data_list)):
            frequency_list = data_list[i].busList[bus_no].frequency
            for j in range(len(pos)):
                pos[j] += step
            bins = sort_bin(frequency_list, lower, middle_left, middle_right, upper)
            canvas.axes.bar(pos, bins, align='center', width=step, label=data_list[i].controllerName)

        for j in range(len(pos)):
            pos[j] -= i * step / 2.0

        canvas.axes.set_xticklabels(bounds)
        canvas.axes.set_xticks(pos)
        canvas.axes.set_xlabel('Frequency (' + data_list[0].busList[bus_no].frequency_unit + ')')
        canvas.axes.set_ylabel('Number of Occurrences')
        canvas.axes.legend(loc='upper right')

    @staticmethod
    def frequency_stats(data, bus_no):
        stats = [np.std(data.busList[bus_no].frequency), np.mean(data.busList[bus_no].frequency)]
        return stats


def sort_bin(data_list, lower_bound, middle_left, middle_right, upper_bound):
    bins = [0, 0, 0, 0, 0]
    for i in range(len(data_list)):

        if data_list[i] < lower_bound:
            bins[0] += 1
        elif (data_list[i] >= lower_bound) & (data_list[i] <= middle_left):
            bins[1] += 1
        elif (data_list[i] >= middle_left) & (data_list[i] <= middle_right):
            bins[2] += 1
        elif (data_list[i] >= middle_right) & (data_list[i] <= upper_bound):
            bins[3] += 1
        elif data_list[i] > upper_bound:
            bins[4] += 1

    return bins


