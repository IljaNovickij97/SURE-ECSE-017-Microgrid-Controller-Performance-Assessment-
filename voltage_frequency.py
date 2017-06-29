import numpy as np


class VoltageAndFrequency(object):

    @staticmethod
    def voltage_time_plot(data_list, canvas, busNo):

        for i in range(len(data_list)):
            canvas.axes.plot(data_list[i].busList[busNo].voltage_time,
                             data_list[i].busList[busNo].voltage, linewidth=1.0)
            if data_list[i].nBus == 0:
                return -1

        time_list = data_list[0].timeList

        voltage_list = []
        for i in range(len(data_list)):
            voltage_list.append(data_list[i].busList[busNo].voltage)
            if voltage_list[i] is None:
                return i

        for i in range(len(data_list)):

            canvas.axes.plot(time_list, voltage_list[i], linewidth=1.0)
            canvas.axes.axis([0, max(time_list) + 1, min(voltage_list[i]) - 1, max(voltage_list[i]) + 1])

        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('Voltage (pu)')

    @staticmethod
    def voltage_hist(data_list, canvas, busNo, step):
        bounds = ['<0.94', '0.94-0.98', '0.98-1.02', '1.02-1.06', '>1.06']
        pos = [0.0, 1.0, 2.0, 3.0, 4.0]

        for i in range(len(data_list)):
            voltage_list = data_list[i].busList[busNo].voltage
            for j in range(len(pos)):
                pos[j] += step
            bins = sort_bin(voltage_list, 0.94, 0.98, 1.02, 1.06)
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
    def frequency_hist(data_list, canvas, bus_no, step):

        bounds = ['<58.5', '58.5-59.5', '59.5-60.5', '60.5-61.5', '>61.5']
        pos = [0.0, 1.0, 2.0, 3.0, 4.0]

        for i in range(len(data_list)):
            frequency_list = data_list[i].busList[bus_no].frequency
            for j in range(len(pos)):
                pos[j] += step
            bins = sort_bin(frequency_list, 58.5, 59.5, 60.5, 61.5)
            canvas.axes.bar(pos, bins, align='center', width=step, label=data_list[i].controllerName)

        for j in range(len(pos)):
            pos[j] -= i * step / 2.0

        canvas.axes.set_xticklabels(bounds)
        canvas.axes.set_xticks(pos)
        canvas.axes.set_xlabel('Frequency (Hz)')
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


