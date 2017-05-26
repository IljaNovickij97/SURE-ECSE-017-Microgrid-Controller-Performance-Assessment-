from __future__ import division
import numpy as np


class Data(object):
    def __init__(self, filename):
        self.filename = filename
        self.busList = []           # Contains the bus objects
        self.derList = []           # Contains the DER objects
        self.loadList = []          # Contains the load objects
        self.timeList = []          # An array of time points. Might be redundant once sampling period/rate is variable
        self.samplingRate = 0       # Sampling rate of data. Might be redundant once sampling period/rate is variable
        self.samplingPeriod = 0     # Sampling period of data. Might be redundant once sampling period/rate is variable
        self.controllerName = ''    # The name of the microgrid controller tested
        self.nBus = 0               # Number of buses in the system
        self.nDer = 0               # Number of DERs in the system
        self.nLoad = 0              # Number of loads in the system

        self.read_data()

    def read_data(self):            # This method parses the file and arranges the data.
                                    # At the moment the parsing is very simplistic. Relies heavily on making sure that
                                    # the file is correct. Might be worth adding redundancy later on.

        f = open(self.filename, 'r', 1)

        # Skips Controller identifier
        f.read(len('Controller '))
        self.controllerName = f.readline()
        self.controllerName = list(self.controllerName)
        self.controllerName.pop()
        self.controllerName = "".join(self.controllerName)

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

        # Very simple placeholder for timeList. Will have to be modified later.
        self.timeList = np.linspace(0, self.samplingPeriod, self.samplingPeriod / self.samplingRate)

        f.close()

    def read_bus(self, f):          # Method used to read in all the necessary values for a bus
        # Skips Voltage identifier
        f.read(len('Voltage '))
        voltage = self.read_values(f)

        # Skips Frequency identifier
        f.read(len('Frequency '))
        frequency = self.read_values(f)

        return Bus(voltage, frequency)

    def read_der(self, f):          # Method used to read in all the necessary values for a DER
        # Skips Type identifier
        f.read(len('Type '))
        energy_type = f.readline()
        energy_type = list(energy_type)
        energy_type.pop()
        energy_type = "".join(energy_type)

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

    def read_load(self, f):         # Method used to read in all the necessary values for a load
        # Skips Type identifier
        f.read(len('Type '))
        load_type = f.readline()
        load_type = list(load_type)
        load_type.pop()
        load_type = "".join(load_type)

        # Skips Power Output identifier
        f.read(len('Power Demand '))
        demand = self.read_values(f)

        return Load(load_type, demand)

    @staticmethod
    def read_values(f):             # Method used to read in an array of values and convert them to floats
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

