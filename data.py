class Data(object):
    def __init__(self, filename):
        self.filename = filename
        self.busList = []
        self.derList = []
        self.loadList = []
        self.samplingRate = 0
        self.samplingPeriod = 0
        self.controllerName = ''
        self.nBus = 0
        self.nDer = 0
        self.nLoad = 0

        self.read_data()

    def read_data(self):
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
        energy_type = f.readline(f)

        # Skips Power Output identifier
        f.read(len('Power Output '))
        output = self.read_values(f)

        # Skips Capacity identifier
        f.read(len('Generation Capacity '))
        capacity = int(f.readline(f))

        # Skips Capacity identifier
        f.read(len('Consumption '))
        consumption = self.read_values(f)

        return Der(energy_type, output, capacity, consumption)

    def read_load(self, f):
        # Skips Type identifier
        f.read(len('Type '))
        load_type = f.readline(f)

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

    def get_voltage(self):
        return self.voltage

    def get_frequency(self):
        return self.frequency


class Der(object):
    def __init__(self, energy_type, output, capacity, consumption):
        self.energy_type = energy_type
        self.output = output
        self.capacity = capacity
        self.consumption = consumption

    def get_energy_type(self):
        return self.energy_type

    def get_output(self):
        return self.output

    def get_capacity(self):
        return self.capacity

    def get_consumption(self):
        return self.consumption


class Load(object):
    def __init__(self, load_type, demand):
        self.load_type = load_type
        self.demand = demand

    def get_type(self):
        return self.load_type

    def get_demand(self):
        return self.demand
