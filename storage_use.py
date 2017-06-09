import numpy as np


class StorageUse(object):

    @staticmethod
    def charge_hist(data_list, canvas, step):
        bounds = ['<20%', '20%-40%', '40%-60%', '60%-80%', '>80%']
        pos = [0.0, 1.0, 2.0, 3.0, 4.0]
        for i in range(len(data_list)):
            n = 0
            charge_state = np.array([0.0] * data_list[i].samplingPeriod)
            for j in range(len(pos)):
                pos[j] += step
            for k in range(0, data_list[i].nDer):
                if data_list[i].derList[k].energy_type == 'Storage':
                    n += 1
                    charge_state += data_list[i].derList[k].consumption
            for k in range(0, len(charge_state)):
                charge_state[k] /= n
            bins = sort_bin(charge_state, 0.2, 0.4, 0.6, 0.8)
            canvas.axes.bar(pos, bins, align='center', width=step, label=data_list[i].controllerName)

        for j in range(len(pos)):
            pos[j] -= i * step / 2.0

        canvas.axes.set_xticklabels(bounds)
        canvas.axes.set_xticks(pos)
        canvas.axes.set_xlabel('State of Charge')
        canvas.axes.set_ylabel('Number of Occurrences')
        canvas.axes.legend(loc='upper right')

    @staticmethod
    def charge_time_plot(data_list, canvas):
        for i in range(len(data_list)):
            k = 0
            for j in range(0, data_list[i].nDer):
                if data_list[i].derList[j].energy_type == 'Storage':
                    k += 1
                    charge_state = data_list[i].derList[j].consumption
                    charge_state_percent = [0.0] * len(charge_state)
                    for m in range(len(charge_state)):
                        charge_state_percent[m] = charge_state[m]*100.0
                    label = 'Storage #' + ("%d " % k) + data_list[i].controllerName
                    canvas.axes.plot(data_list[i].timeList, charge_state_percent, label=label, linewidth=1.0)

        canvas.axes.set_xlabel("Time (s)")
        canvas.axes.set_ylabel("State of Charge (%)")
        canvas.axes.legend(loc='upper right')
        canvas.axes.set_xlim([0, len(data_list[i].timeList) - 1])

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


def sort_bin(data_list, lower_bound, middle_left, middle_right, upper_bound):
    bins = [0, 0, 0, 0, 0]
    for i in range(len(data_list)):

        if data_list[i] < lower_bound:
            bins[0] += 1
        elif (data_list[i] >= lower_bound) & (data_list[i] <= middle_left):
            bins[1] += 1
        elif (data_list[i] >= middle_left) & (data_list[i] <= middle_right):
            bins[2] += 1
        elif (data_list[i] >= middle_right) & (data_list[i] <= upper_bound):
            bins[3] += 1
        elif data_list[i] > upper_bound:
            bins[4] += 1

    return bins

