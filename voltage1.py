import numpy as np

class voltageAndFrequency(object):

    @staticmethod
    def voltageTimePlot(data, canvas, busNo):
        voltageList = data.busList[busNo].voltage
        timeList = data.timeList
        canvas.axes = canvas.fig.add_subplot(111)
        canvas.axes.plot(timeList, voltageList)
        canvas.axes.axis([0, max(timeList) + 1, min(voltageList) - 1, max(voltageList) + 1])
        return

    @staticmethod
    def voltageHist(data, canvas, busNo, step):
        voltageList = data.busList[busNo].voltage
        partition = int((max(voltageList) - min(voltageList)) / step)
        hist, bins = np.histogram(voltageList, partition, density =False)
        center = (bins[:-1] + bins[1:]) / 2
        canvas.axes = canvas.fig.add_subplot(111)
        canvas.axes.bar(center, hist, align='center', width=step)

    def test(self, data):
        timeList = data.timeList
        self.voltageGraph(0, timeList)

