class Voltage(object):
    def __init__(self, data, canvas, busNo):

        canvas.axes = canvas.fig.add_subplot(111)
        voltageList = data.busList[busNo].voltage
        timeList = data.timeList
        canvas.axes.plot(timeList, voltageList, linestyle='--', color='red')
        canvas.axes.axis([0, max(timeList)+1, min(voltageList)-1, max(voltageList)+1])

