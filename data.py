from __future__ import division
import numpy as np
import h5py


class Data(object):
    def __init__(self, filename):
        self.filename = filename
        self.f = None               # File handle
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
        self.temp_label_list = []   # List of labels for when mat data needs to be sorted
        self.temp_index = []        # Index used to find and sort unlabelled mat data
        self.main_label_list = []
        self.done_flag = False      # Flag used to tell gui.py whether data is fully sorted and loaded

        if filename[-3:] == 'txt':
            self.read_text_data()
        elif filename[-3:] == 'mat':
            try:
                self.read_labelled_mat_data()
            except OSError:
                raise OSError
            except:
                self.read_unlabelled_mat_data()

    def read_text_data(self):       # This method parses the file and arranges the data.
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
            self.busList.append(self.read_text_bus(f))
            f.readline()

        for i in range(self.nDer):
            self.derList.append(self.read_text_der(f))
            f.readline()

        for i in range(self.nLoad):
            self.loadList.append(self.read_text_load(f))
            f.readline()

        # Very simple placeholder for timeList. Will have to be modified later.
        self.timeList = np.linspace(0, self.samplingPeriod, int(self.samplingPeriod / self.samplingRate))

        # more realistic/robust timeList, unless already provided
        for i in range(self.nBus):
            if (self.busList[i].voltage_time is None) or (self.busList[i].frequency_time is None):
                self.busList[i].voltage_time, self.busList[i].frequency_time, self.timeList = [], [], []
                for j in range(self.samplingPeriod * self.samplingRate):
                    self.busList[i].voltage_time.append(j / self.samplingRate)
                    self.busList[i].frequency_time.append(j / self.samplingRate)
                    self.timeList.append(j / self.samplingRate)

        f.close()
        self.done_flag = True

    def read_text_bus(self, f):          # Method used to read in all the necessary values for a bus
        # Skips Voltage identifier
        f.read(len('Voltage '))
        voltage = self.read_text_values(f)

        # Skips Frequency identifier
        f.read(len('Frequency '))
        frequency = self.read_text_values(f)

        return Bus(voltage, frequency)

    def read_text_der(self, f):          # Method used to read in all the necessary values for a DER
        # Skips Type identifier
        f.read(len('Type '))
        energy_type = f.readline()
        energy_type = list(energy_type)
        energy_type.pop()
        energy_type = "".join(energy_type)

        # Skips Power Output identifier
        f.read(len('Power Output '))
        output = self.read_text_values(f)

        # Skips Capacity identifier
        f.read(len('Generation Capacity '))
        capacity = int(f.readline())

        # Skips Capacity identifier
        f.read(len('Consumption '))
        consumption = self.read_text_values(f)

        return Der(energy_type, output, capacity, consumption)

    def read_text_load(self, f):         # Method used to read in all the necessary values for a load
        # Skips Type identifier
        f.read(len('Type '))
        load_type = f.readline()
        load_type = list(load_type)
        load_type.pop()
        load_type = "".join(load_type)

        # Skips Power Output identifier
        f.read(len('Power Demand '))
        demand = self.read_text_values(f)

        return Load(load_type, demand)

    @staticmethod
    def read_text_values(f):             # Method used to read in an array of values and convert them to floats
        string = f.readline()
        if string == ' ':
            return
        string = string.split(' ')

        for i in range(len(string)):
            string[i] = float(string[i])
        return string

    def read_labelled_mat_data(self):            # Method used to read in data from a .mat file
        f = h5py.File(self.filename, 'r')

        # Get references for data id and label locations
        data_ref = np.array(f.get('SDIDescriptor/Signals/DataID'))
        label_ref = np.array(f.get('SDIDescriptor/Signals/SignalLabel'))
        name_ref = f['SDIDescriptor/Runs/RunName'].value
        self.controllerName = []
        for i in range(len(name_ref)):
            self.controllerName.append(chr(name_ref[i][0]))

        self.controllerName = ''.join(self.controllerName)
        print(self.controllerName)

        for i in range(len(data_ref)):
            # Read in the label and store it in a string
            current_label = f[label_ref[i][0]]
            label = []
            for j in range(len(current_label)):
                label.append(chr(current_label[j][0]))
            label = "".join(label)

            if 'V-bus' in label:
                current_bus = int(self.get_word(label, 1)[3:])
                while current_bus > self.nBus:
                    self.nBus += 1
                    self.busList.append(Bus())

                current_signal = f[data_ref[i][0]]
                string1 = 's' + str(current_signal[0][0]) + '/DataValues'
                string2 = 's' + str(current_signal[0][0]) + '/TimeValues'
                self.busList[current_bus - 1].voltage = np.array(f.get(string1))[0]
                self.busList[current_bus - 1].voltage_time = np.transpose(np.array(f.get(string2)))[0]
                self.busList[current_bus - 1].voltage_unit = self.get_word(label, 2)

            elif 'F-bus' in label:
                current_bus = int(self.get_word(label, 1)[3:])
                while current_bus > self.nBus:
                    self.nBus += 1
                    self.busList.append(Bus())

                current_signal = f[data_ref[i][0]]
                string1 = 's' + str(current_signal[0][0]) + '/DataValues'
                string2 = 's' + str(current_signal[0][0]) + '/TimeValues'
                self.busList[current_bus - 1].frequency = np.array(f.get(string1))[0]
                self.busList[current_bus - 1].frequency_time = np.transpose(np.array(f.get(string2)))[0]
                self.busList[current_bus - 1].frequency_unit = self.get_word(label, 2)

            elif 'Po-der' in label:
                current_der = int(self.get_word(label, 1)[3:])
                while current_der > self.nDer:
                    self.nDer += 1
                    self.derList.append(Der())

                current_signal = f[data_ref[i][0]]
                string1 = 's' + str(current_signal[0][0]) + '/DataValues'
                string2 = 's' + str(current_signal[0][0]) + '/TimeValues'
                self.derList[current_der - 1].output = np.array(f.get(string1))[0]
                self.derList[current_der - 1].time = np.transpose(np.array(f.get(string2)))[0]
                self.derList[current_der - 1].energy_type = self.get_word(label, 2)
                self.derList[current_der - 1].capacity = int(self.get_word(label, 3))
                self.derList[current_der - 1].output_unit = self.get_word(label, 4)

            elif 'C-der' in label:
                current_der = int(self.get_word(label, 1)[3:])
                while current_der > self.nDer:
                    self.nDer += 1
                    self.derList.append(Der())

                current_signal = f[data_ref[i][0]]
                string1 = 's' + str(current_signal[0][0]) + '/DataValues'
                self.derList[current_der - 1].consumption = np.array(f.get(string1))[0]
                self.derList[current_der - 1].consumpion_unit = self.get_word(label, 2)

            elif 'SOC-der' in label:
                current_der = int(self.get_word(label, 1)[3:])
                while current_der > self.nDer:
                    self.nDer += 1
                    self.derList.append(Der())

                current_signal = f[data_ref[i][0]]
                string1 = 's' + str(current_signal[0][0]) + '/DataValues'
                self.derList[current_der - 1].consumption = np.array(f.get(string1))[0]

            elif 'Pd-load' in label:
                current_load = int(self.get_word(label, 1)[4:])
                while current_load > self.nLoad:
                    self.nLoad += 1
                    self.loadList.append(Load())

                current_signal = f[data_ref[i][0]]
                string1 = 's' + str(current_signal[0][0]) + '/DataValues'
                string2 = 's' + str(current_signal[0][0]) + '/TimeValues'
                self.loadList[current_load - 1].demand = np.array(f.get(string1))[0]
                self.loadList[current_load - 1].time = np.transpose(np.array(f.get(string2)))[0]
                self.loadList[current_load - 1].load_type = self.get_word(label, 2)
                self.loadList[current_load - 1].unit = self.get_word(label, 3)

            else:
                continue

        self.done_flag = True

    def read_unlabelled_mat_data(self):
        self.f = h5py.File(self.filename, 'r')

        def all(name):
            self.main_label_list.append(name)
            return None
        self.f.visit(all)

        for i in range(len(self.main_label_list)):
            current_data = self.f['/' + self.main_label_list[i]]
            if current_data.shape[1] > 1:
                index = []
                for j in range(current_data.shape[1]):
                    self.temp_label_list.append(self.main_label_list[i] + ' Row ' + str(j + 1))
                    index.append(j)
                self.temp_index.append(index)
            else:
                self.temp_label_list.append(self.main_label_list[i])
                self.temp_index.append([0])

    def sort_labelled_data(self):
        for i in range(len(self.main_label_list)):
            current_data = np.array(self.f.get('/' + self.main_label_list[i]))
            for j in self.temp_index[i]:
                current_signal = current_data[:, j]
                label = self.temp_label_list[i][j]

                if 'T' in label:
                    self.timeList = current_signal
                    self.samplingPeriod = self.timeList[-1]

                elif 'V-bus' in label:
                    current_bus = int(self.get_word(label, 1)[3:])
                    while current_bus > self.nBus:
                        self.nBus += 1
                        self.busList.append(Bus())

                    self.busList[current_bus - 1].voltage = current_signal
                    self.busList[current_bus - 1].voltage_unit = self.get_word(label, 2)

                elif 'F-bus' in label:
                    current_bus = int(self.get_word(label, 1)[3:])
                    while current_bus > self.nBus:
                        self.nBus += 1
                        self.busList.append(Bus())

                    self.busList[current_bus - 1].frequency = current_signal
                    self.busList[current_bus - 1].frequency_unit = self.get_word(label, 2)

                elif 'Po-der' in label:
                    current_der = int(self.get_word(label, 1)[3:])
                    while current_der > self.nDer:
                        self.nDer += 1
                        self.derList.append(Der())

                    self.derList[current_der - 1].output = current_signal
                    self.derList[current_der - 1].energy_type = self.get_word(label, 2)
                    self.derList[current_der - 1].capacity = int(self.get_word(label, 3))
                    self.derList[current_der - 1].output_unit = self.get_word(label, 4)

                elif 'C-der' in label:
                    current_der = int(self.get_word(label, 1)[3:])
                    while current_der > self.nDer:
                        self.nDer += 1
                        self.derList.append(Der())

                    self.derList[current_der - 1].consumption = current_signal
                    self.derList[current_der - 1].consumpion_unit = self.get_word(label, 2)

                elif 'SOC-der' in label:
                    current_der = int(self.get_word(label, 1)[3:])
                    while current_der > self.nDer:
                        self.nDer += 1
                        self.derList.append(Der())

                    self.derList[current_der - 1].consumption = current_signal

                elif 'Pd-load' in label:
                    current_load = int(self.get_word(label, 1)[4:])
                    while current_load > self.nLoad:
                        self.nLoad += 1
                        self.loadList.append(Load())

                    self.loadList[current_load - 1].demand = current_signal
                    self.loadList[current_load - 1].load_type = self.get_word(label, 2)
                    self.loadList[current_load - 1].unit = self.get_word(label, 3)

                else:
                    continue
        self.fill_time_lists()
        self.print_all()
        self.done_flag = True

    def fill_time_lists(self):
        for i in range(self.nBus):
            if self.busList[i].voltage_time == None and not self.busList[i].frequency == None:
                self.busList[i].voltage_time = np.linspace(0, self.samplingPeriod, len(self.busList[i].voltage))
            if self.busList[i].frequency_time == None and not self.busList[i].frequency == None:
                self.busList[i].frequency_time = np.linspace(0, self.samplingPeriod, len(self.busList[i].frequency))

            for i in range(self.nDer):
                if self.derList[i].time == None and not self.derList[i].output == None:
                    self.derList[i].time = np.linspace(0, self.samplingPeriod, len(self.derList[i].output))

            for i in range(self.nLoad):
                if self.loadList[i].time == None and not self.derList[i].demand == None:
                    self.derList[i].time = np.linspace(0, self.samplingPeriod, len(self.loadList[i].demand))

    @staticmethod
    def get_word(label, start):             # Method used to get a specific word from a label
        flag = 0
        label_type = []
        for i in range(len(label)):
            if '-' in label[i]:
                flag += 1
                if flag > start:
                    break
            elif flag == start:
                label_type.append(label[i])

        label_type = "".join(label_type)
        return label_type

    def print_all(self):                    # Used to debug data
        for i in range(len(self.busList)):
            label = "Bus: " + str(i + 1)
            print(label)
            print(self.busList[i].voltage)
            print(self.busList[i].voltage_time)
            print(self.busList[i].voltage_unit)
            print(self.busList[i].frequency)
            print(self.busList[i].frequency_time)
            print(self.busList[i].frequency_unit)

        for i in range(len(self.derList)):
            label = "Der: " + str(i + 1)
            print(label)
            print(self.derList[i].output)
            print(self.derList[i].time)
            print(self.derList[i].output_unit)
            print(self.derList[i].consumption)
            print(self.derList[i].consumption_unit)
            print(self.derList[i].energy_type)
            print(self.derList[i].capacity)

        for i in range(len(self.loadList)):
            label = "Load: " + str(i + 1)
            print(label)
            print(self.loadList[i].demand)
            print(self.loadList[i].time)
            print(self.loadList[i].unit)
            print(self.loadList[i].load_type)

    def check_vf(self):
        if self.nBus == 0:
            return False
        for i in range(self.nBus):
            if self.busList[i].voltage == None:
                return False
            elif self.busList[i].voltage_time == None:
                return False
            elif self.busList[i].frequency == None:
                return False
            elif self.busList[i].frequency_time == None:
                return False

        return True

    def check_gr(self):
        if self.nLoad == 0:
            return False
        for i in range(self.nLoad):
            if 'Dump' in self.loadList[i].load_type:
                return True

        return False

    def check_rei(self):
        if self.nDer == 0:
            return False
        else:
            return True

    def check_rc(self):
        fuel_index = []
        for i in range(self.nDer):
            if 'Fuel' in self.derList[i].energy_type:
                fuel_index.append(i)

        if len(fuel_index) == 0:
            return False

        for i in range(len(fuel_index)):
            if self.derList[fuel_index[i]].output is None:
                return False
            elif self.derList[fuel_index[i]].consumption is None:
                return False

        return True

    def check_su(self):
        storage_index = []
        for i in range(self.nDer):
            if 'Storage' in self.derList[i].energy_type:
                storage_index.append(i)

        if len(storage_index) == 0:
            return False

        for i in range(len(storage_index)):
            if self.derList[storage_index[i]].consumption is None:
                return False

        return True

    # Method used to turn matrix rows into vectors for use in data selection
    @staticmethod
    def disassemble_matrix(matrix):
        vector_list = []

        for i in range(np.shape(matrix)[1]):
            vector = matrix[:, i]
            vector_list.append(vector)

        return vector_list


class Bus(object):
    def __init__(self, voltage=None, frequency=None):
        self.voltage = voltage
        self.frequency = frequency
        self.voltage_time = None
        self.frequency_time = None
        self.voltage_unit = 'pu'
        self.frequency_unit = 'Hz'


class Der(object):
    def __init__(self, energy_type=None, output=None, capacity=None, consumption=None):
        self.energy_type = energy_type
        self.output = output
        self.capacity = capacity
        self.consumption = consumption
        self.time = None
        self.output_unit = None
        self.consumption_unit = None


class Load(object):
    def __init__(self, load_type=None, demand=None):
        self.load_type = load_type
        self.demand = demand
        self.time = None
        self.unit = None
