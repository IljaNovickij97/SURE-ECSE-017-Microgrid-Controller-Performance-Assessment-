import numpy as np

class StorageUse(object):

    @staticmethod
    def charge_time_plot(data_list, canvas):
        for i in range(len(data_list)):
            total_capacity = 0.0
            stored_energy = np.array([0.0]*len(data_list[i].timeList))
            power_flow = np.array([0.0]*len(data_list[i].timeList))
            for j in range(0, data_list[i].nDer):
                if data_list[i].derList[j].energy_type == 'Battery':
                    power_flow += np.array(data_list[i].derList[j].output)
                    total_capacity += data_list[i].derList[j].capacity

            stored_energy[0] = 0
            for j in range(1, len(power_flow)):
                    stored_energy[j] = stored_energy[j - 1] - power_flow[j - 1]
            charge_state = (100*stored_energy) / (total_capacity*60*60)
            canvas.axes.plot(data_list[i].timeList, charge_state, label=data_list[i].controllerName)

        canvas.axes.set_xlabel("Time (s)")
        canvas.axes.set_ylabel("State of Charge (%)")
        canvas.axes.legend(loc='upper right')

    @staticmethod
    def charge_stats(data):
        time_spent_charging = 0
        time_spent_discharging = 0

        for i in range(0, data.nDer):
            if data.derList[i].energy_type == 'Battery':
                for j in range(0, len(data.derList[i].output)):
                    if data.derList[i].output[j] < 0:
                        time_spent_charging += 1
                    elif data.derList[i].output[j] > 0:
                        time_spent_discharging += 1


