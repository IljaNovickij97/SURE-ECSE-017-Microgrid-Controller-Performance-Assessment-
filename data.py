from __future__ import division


def linspace(start, stop, n):
    space = []
    if n == 1:
        return
    h = (stop - start) / (n - 1)
    for i in range(int(n)):
        space.append(start + h * i)

    return space


class Data(object):
    def __init__(self, filename):
        self.filename = filename
        self.busList = []
        self.derList = []
        self.loadList = []
        self.timeList = []
        self.samplingRate = 0
        self.samplingPeriod = 0
        self.controllerName = ''
        self.nBus = 0
        self.nDer = 0
        self.nLoad = 0

        self.read_data()

    def read_data(self):
        #### This whole method needs work. Add in checks for errors etc.
        f = open(self.filename, 'r', 1)

        # Skips Controller identifier
        f.read(len('Controller '))
        self.controllerName = f.readline()

        # Skips Sampling Rate identifier
        f.read(len('Sampling Rate '))
        self.samplingRate = int(f.readline())

        # Skips Sampling Period identifier
        f.read(len('Sampling Period '))
        self.samplingPeriod = int(f.readline())

        # Should read '### System info'
        f.readline()

        # Skips Bus No. identifier
        f.read(len('Bus No. '))
        self.nBus = int(f.readline())

        # Skips DER No. identifier
        f.read(len('DER No. '))
        self.nDer = int(f.readline())

        # Skips Load No. identifier
        f.read(len('Load No. '))
        self.nLoad = int(f.readline())

        # Should read '### Bus info'
        f.readline()

        for i in range(self.nBus):
            self.busList.append(self.read_bus(f))
            f.readline()

        for i in range(self.nDer):
            self.derList.append(self.read_der(f))
            f.readline()

        for i in range(self.nLoad):
            self.loadList.append(self.read_load(f))
            f.readline()

        self.timeList = linspace(1, self.samplingPeriod, self.samplingPeriod / self.samplingRate)

    def read_bus(self, f):
        # Skips Voltage identifier
        f.read(len('Voltage '))
        voltage = self.read_values(f)

        # Skips Frequency identifier
        f.read(len('Frequency '))
        frequency = self.read_values(f)

        return Bus(voltage, frequency)

    def read_der(self, f):
        # Skips Type identifier
        f.read(len('Type '))
        energy_type = f.readline()

        # Skips Power Output identifier
        f.read(len('Power Output '))
        output = self.read_values(f)

        # Skips Capacity identifier
        f.read(len('Generation Capacity '))
        capacity = int(f.readline())

        # Skips Capacity identifier
        f.read(len('Consumption '))
        consumption = self.read_values(f)

        return Der(energy_type, output, capacity, consumption)

    def read_load(self, f):
        # Skips Type identifier
        f.read(len('Type '))
        load_type = f.readline()

        # Skips Power Output identifier
        f.read(len('Power Demand '))
        demand = self.read_values(f)

        return Load(load_type, demand)

    @staticmethod
    def read_values(f):
        string = f.readline()
        string = string.split(' ')

        for i in range(len(string)):
            string[i] = float(string[i])
        return string


class Bus(object):
    def __init__(self, voltage, frequency):
        self.voltage = voltage
        self.frequency = frequency



class Der(object):
    def __init__(self, energy_type, output, capacity, consumption):
        self.energy_type = energy_type
        self.output = output
        self.capacity = capacity
        self.consumption = consumption



class Load(object):
    def __init__(self, load_type, demand):
        self.load_type = load_type
        self.demand = demand

