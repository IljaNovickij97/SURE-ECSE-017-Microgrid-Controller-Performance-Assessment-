import numpy as np


class VoltageAndFrequency(object):

    @staticmethod
    def voltage_time_plot(data_list, canvas, busNo):
        voltageList = data_list[0].busList[busNo].voltage
        timeList = np.linspace(0, len(voltageList) - 1, len(voltageList))

        for i in range(len(data_list)):
            voltageList = data_list[i].busList[busNo].voltage
            canvas.axes.plot(timeList, voltageList)
            canvas.axes.axis([0, max(timeList) + 1, min(voltageList) - 1, max(voltageList) + 1])

        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('Voltage (V)')

    @staticmethod
    def voltage_hist(data_list, canvas, busNo, step):
        bounds = ['<120', '120-180', '180-220', '220-260', '>260']
        pos = [0.0, 1.0, 2.0, 3.0, 4.0]

        for i in range(len(data_list)):
            voltageList = data_list[i].busList[busNo].voltage
            for j in range(len(pos)):
                pos[j] += step
            bins = sort_bin(voltageList, 120, 180, 220, 260)
            canvas.axes.bar(pos, bins, align='center', width=step, label=data_list[i].controllerName)

        for j in range(len(pos)):
            pos[j] -= i * step / 2.0

        canvas.axes.set_xticklabels(bounds)
        canvas.axes.set_xticks(pos)
        canvas.axes.set_xlabel('Voltage (V)')
        canvas.axes.set_ylabel('Number of Occurrences')
        canvas.axes.legend(loc='upper right')

    @staticmethod
    def voltage_stats(data, busNo):
        stats = [np.std(data.busList[busNo].voltage), np.mean(data.busList[busNo].voltage)]
        return stats

    @staticmethod
    def frequency_time_plot(data_list, canvas, busNo):
        frequencyList = data_list[0].busList[busNo].frequency
        timeList = np.linspace(0, len(frequencyList) - 1, len(frequencyList))

        for i in range(len(data_list)):
            frequencyList = data_list[i].busList[busNo].frequency
            canvas.axes.plot(timeList, frequencyList)
            canvas.axes.axis([0, max(timeList) + 1, min(frequencyList) - 1, max(frequencyList) + 1])

        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('Frequency (Hz)')

    @staticmethod
    def frequency_hist(data_list, canvas, busNo, step):

        bounds = ['<58.5', '58.5-59.5', '59.5-60.5', '60.5-61.5', '>61.5']
        pos = [0.0, 1.0, 2.0, 3.0, 4.0]

        for i in range(len(data_list)):
            frequencyList = data_list[i].busList[busNo].frequency
            for j in range(len(pos)):
                pos[j] += step
            bins = sort_bin(frequencyList, 58.5, 59.5, 60.5, 61.5)
            canvas.axes.bar(pos, bins, align='center', width=step, label=data_list[i].controllerName)

        for j in range(len(pos)):
            pos[j] -= i * step / 2.0

        canvas.axes.set_xticklabels(bounds)
        canvas.axes.set_xticks(pos)
        canvas.axes.set_xlabel('Frequency (Hz)')
        canvas.axes.set_ylabel('Number of Occurrences')
        canvas.axes.legend(loc='upper right')

    @staticmethod
    def frequency_stats(data, busNo):
        stats = [np.std(data.busList[busNo].frequency), np.mean(data.busList[busNo].frequency)]
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


