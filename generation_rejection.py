import data
import numpy as np


class GenerationRejection(object):

    @staticmethod
    def dump_time_plot(data, canvas):

        dump_loads = []
        dump_load_use  = np.array([0.0]*data.samplingPeriod)

        for i in range(0, data.nLoad):
            if data.loadList[i].load_type == 'Dump':
                dump_loads.append(data.loadList[i])

        for i in range(len(dump_loads)):
                dump_load_use += dump_loads[i].demand

        canvas.axes.plot(data.timeList, dump_load_use)
        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('Dump Load Use (MW)')

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
