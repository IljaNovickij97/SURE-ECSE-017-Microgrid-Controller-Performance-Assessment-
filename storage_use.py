import numpy as np

class StorageUse(object):

    @staticmethod
    def charge_time_plot(data_list, canvas):
        for i in range(len(data_list)):
            k = 0
            for j in range(0, data_list[i].nDer):
                if data_list[i].derList[j].energy_type == 'Storage':
                    k += 1
                    charge_state = data_list[i].derList[j].consumption
                    label = 'Storage #' + ("%d " % k) + data_list[i].controllerName
                    canvas.axes.plot(data_list[i].timeList, charge_state, label=label)

        canvas.axes.set_xlabel("Time (s)")
        canvas.axes.set_ylabel("State of Charge (%)")
        canvas.axes.legend(loc='upper right')

    @staticmethod
    def charge_stats(data):
        time_spent_charging = []
        time_spent_discharging = []
        time_spent_idle = []
        k = -1
        for i in range(0, data.nDer):
            if data.derList[i].energy_type == 'Storage':
                k += 1

                time_spent_charging.append(0)
                time_spent_discharging.append(0)
                time_spent_idle.append(0)

                for j in range(0, len(data.derList[i].output)):
                    if data.derList[i].output[j] < 0:
                        time_spent_charging[k] += 1
                    elif data.derList[i].output[j] > 0:
                        time_spent_discharging[k] += 1
                    else:
                        time_spent_idle[k] += 1

        stats = [time_spent_charging, time_spent_discharging, time_spent_idle]
        return stats

    @staticmethod
    def pure_efficiency_charge_state(data_list):
        charge_state_list = []
        for i in range(len(data_list)):
            total_capacity = 0.0
            stored_energy = np.array([0.0] * len(data_list[i].timeList))
            power_flow = np.array([0.0] * len(data_list[i].timeList))
            for j in range(0, data_list[i].nDer):
                if data_list[i].derList[j].energy_type == 'Storage':
                    power_flow += np.array(data_list[i].derList[j].output)
                    total_capacity += data_list[i].derList[j].capacity

            stored_energy[0] = 0
            for j in range(1, len(power_flow)):
                stored_energy[j] = stored_energy[j - 1] - power_flow[j - 1]
            charge_state = (100 * stored_energy) / (total_capacity * 60 * 60)
            charge_state_list.append(charge_state)




