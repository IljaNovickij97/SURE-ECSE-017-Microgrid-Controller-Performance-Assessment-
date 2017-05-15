def read_values(f):
    string = f.readline()
    string = string.split(' ')
    string.pop()

    for i in range(len(string)):
        string[i] = float(string[i])
    return string

class Data(object):

    def __init__(self, filename):
        self.filename = filename
        self.busList = []
        self.derList = []
        self.loadList = []
        self.samplingRate = 0
        self.samplingPeriod = 0
        self.controllerName = ''

        self.read_data()

    def read_data(self):
        #To do

    def read_bus(self, f):
        #Skips Voltage identifier
        f.read(len('Voltage '))
        voltage = read_values(f)

        #Skips Frequency identifier
        f.read(len('Frequency '))
        frequency = read_values(f)

        return Bus(voltage, frequency)

    def read_der(self, f):
        #Skips Type identifier
        f.read(len('Type '))
        energy_type = (f.readline(f))

        #Skips Power Output identifier
        f.read(len('Power Output '))
        output = read_values(f)

        #Skips Capacity identifier
        f.read(len('Generation Capacity '))
        capacity = int(f.readline(f))

        # Skips Capacity identifier
        f.read(len('Consumption '))
        consumption = read_values(f)

        return Der(energy_type, output, capacity, consumption)

    def read_load(self, f):
        # Skips Type identifier
        f.read(len('Type '))
        load_type = (f.readline(f))

        # Skips Power Output identifier
        f.read(len('Power Demand '))
        demand = read_values(f)

        return Load(load_type, demand)

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


