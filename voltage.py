class voltageAndFrequency(object):
    def __init__(self, data, canvas, busNo):
        voltageList = data.busList[busNo].voltage
        timeList = data.timeList
        canvas.plot(timeList, voltageList)
        canvas.axis([0, max(timeList)+1, min(voltageList)-1, max(voltageList)+1])

