import numpy as np


class VoltageAndFrequency(object):

    @staticmethod
    def voltage_time_plot(data, canvas, busNo):
        canvas.axes = canvas.fig.add_subplot(111)
        voltageList = data.busList[busNo].voltage
        timeList = np.linspace(0, len(voltageList) - 1, len(voltageList))
        canvas.axes.plot(timeList, voltageList)
        canvas.axes.axis([0, max(timeList) + 1, min(voltageList) - 1, max(voltageList) + 1])
        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('Voltage (V)')
        canvas.draw()
        return

    @staticmethod
    def voltage_hist(data, canvas, busNo, step):
        canvas.axes = canvas.fig.add_subplot(111)
        voltageList = data.busList[busNo].voltage
        partition = int((max(voltageList) - min(voltageList)) / step)
        hist, bins = np.histogram(voltageList, partition, density=False)
        center = (bins[:-1] + bins[1:]) / 2
        canvas.axes.bar(center, hist, align='center', width=step)
        canvas.axes.set_xlabel('Voltage (V)')
        canvas.axes.set_ylabel('Number of Occurrences')
        canvas.draw()

    def test(self, data):
        timeList = data.timeList
        self.voltageGraph(0, timeList)
