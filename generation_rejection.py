import data
import numpy as np


class GenerationRejection(object):

    @staticmethod
    def dump_time_plot(data_list, canvas):

        for i in range(len(data_list)):
            dump_loads = []
            dump_load_use = np.array([0.0] * data_list[i].samplingPeriod)
            for j in range(0, data_list[i].nLoad):
                if data_list[i].loadList[j].load_type == 'Dump':
                    dump_loads.append(data_list[i].loadList[j])
            for j in range(len(dump_loads)):
                    dump_load_use += dump_loads[j].demand
            canvas.axes.plot(data_list[i].timeList, dump_load_use, label=data_list[i].controllerName, linewidth=1.0)

        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('Dump Load Use (MW)')
        canvas.axes.legend(loc='upper right')
        canvas.axes.set_xlim([0, len(data_list[i].timeList) - 1])

    @staticmethod
    def dump_stats(data):

        dump_loads = []
        stats = []
        total_dumped = 0

        for i in range(0, data.nLoad):
            if data.loadList[i].load_type == 'Dump':
                dump_loads.append(data.loadList[i])


        for i in range(len(dump_loads)):
            for j in range(0, data.samplingPeriod):
                total_dumped += dump_loads[i].demand[j]

        total_dumped /= (data.samplingPeriod*60*60)
        stats.append(total_dumped)

        return stats
