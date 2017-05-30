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
        voltageList = data_list[0].busList[busNo].voltage
        partition = int((max(voltageList) - min(voltageList)) / step)

        for i in range(len(data_list)):
            voltageList = data_list[i].busList[busNo].voltage
            hist, bins = np.histogram(voltageList, partition, density=False)
            if i == 0:
                center = (bins[:-1] + bins[1:]) / 2
            canvas.axes.bar(center, hist, align='center', width=step)

        canvas.axes.set_xlabel('Voltage (V)')
        canvas.axes.set_ylabel('Number of Occurrences')

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
        frequencyList = data_list[0].busList[busNo].frequency
        partition = int((max(frequencyList) - min(frequencyList)) / step)

        for i in range(len(data_list)):
            frequencyList = data_list[i].busList[busNo].frequency
            hist, bins = np.histogram(frequencyList, partition, density=False)
            center = ((bins[:-1] + bins[1:]) / 2) + i*step
            canvas.axes.bar(center, hist, align='center', width=step)

        canvas.axes.set_xlabel('Frequency (Hz)')
        canvas.axes.set_ylabel('Number of Occurrences')

    @staticmethod
    def frequency_stats(data, busNo):
        stats = [np.std(data.busList[busNo].frequency), np.mean(data.busList[busNo].frequency)]
        return stats


