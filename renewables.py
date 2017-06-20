from pylab import *
import numpy as np
# **assume all possible DER types are Fuel (Diesel, Gas, Propane...), Renewable (Wind, Hydro, PV...), and Storage **


class Renewables(object):

    @staticmethod
    def renewable_pie(data, canvas):
        t = data.timeList

        # List of all generation types - completely arbitrary, expandable
        gen_types = []
        for i in range(data.nDer):
            if 'Storage' not in data.derList[i].energy_type:
                gen_types.append(data.derList[i].energy_type)

        gen_types = list(set(gen_types))

        # if no data found, return 0 for robustness
        if not gen_types:
            return 0

        num_gen = len(gen_types)
        gen_list = np.array([[0.0]*len(t) for j in range(num_gen)])

        for i in range(num_gen):
            # temp variable to hold total gen of one type
            temp_gen = np.array([0.0] * len(t))
            for x in range(data.nDer):
                if data.derList[x].energy_type == gen_types[i]:
                    temp_gen += np.array(data.derList[x].output)
                gen_list[i] = temp_gen

        # list of generation proportions that will be used for the pie chart
        chart_list = np.array([0.0]*num_gen)
        for i in range(num_gen):
            # total generation per type
            chart_list[i] = sum(gen_list[i])

        explode = []
        for i in range(num_gen):
            if 'Fuel' in gen_types[i]:
                explode.append(0)
            elif 'Ren' in gen_types[i]:
                explode.append(0.1)

        colors = ['magenta', 'lightskyblue', 'gold', 'lime', 'cyan', 'yellowgreen', 'lightcoral', 'deeppink']
        colors = colors[:num_gen]

        labels = []
        for i in range(num_gen):
            if 'Fuel' in gen_types[i]:
                labels.append(gen_types[i][5:])
            elif 'Ren' in gen_types[i]:
                labels.append(gen_types[i][4:])

        title = data.controllerName + ' Absolute Energy Distribution'
        canvas.axes.set_title(title)
        canvas.axes.pie(chart_list, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)

    @staticmethod
    def renewable_norm_pie(data, canvas):
        t = data.timeList

        # List of all generation types - completely arbitrary, expandable
        gen_types = []
        for i in range(data.nDer):
            if 'Storage' not in data.derList[i].energy_type:
                gen_types.append(data.derList[i].energy_type)

        gen_types = list(set(gen_types))
        num_gen = len(gen_types)
        gen_list = np.array([[0.0] * len(t) for j in range(num_gen)])
        cap_list = [0]*num_gen

        for i in range(num_gen):
            # temp variable to hold total gen of one type
            temp_gen = np.array([0.0] * len(t))
            temp_cap = 0
            for x in range(data.nDer):
                if data.derList[x].energy_type == gen_types[i]:
                    temp_gen += np.array(data.derList[x].output)
                    temp_cap += data.derList[x].capacity
                gen_list[i] = temp_gen
                cap_list[i] = temp_cap

        # list of generation proportions that will be used for the pie chart
        chart_list = np.array([0.0] * num_gen)
        for i in range(num_gen):
            # total generation per type
            chart_list[i] = (sum(gen_list[i]))/cap_list[i]

        explode = []
        for i in range(num_gen):
            if 'Fuel' in gen_types[i]:
                explode.append(0)
            elif 'Ren' in gen_types[i]:
                explode.append(0.1)

        colours = ['magenta', 'lightskyblue', 'gold', 'lime', 'cyan', 'yellowgreen', 'lightcoral', 'deeppink']
        colours = colours[:num_gen]

        labels = []
        for i in range(num_gen):
            if 'Fuel' in gen_types[i]:
                labels.append(gen_types[i][5:])
            elif 'Ren' in gen_types[i]:
                labels.append(gen_types[i][4:])

        title = data.controllerName + ' Normalized Energy Distribution'
        canvas.axes.set_title(title)
        canvas.axes.pie(chart_list, explode=explode, labels=labels, colors=colours, autopct='%1.1f%%', startangle=90)

    # The below method is currently unused. If used, DER types need to be adjusted.
    @staticmethod
    def renewable_time(data, canvas):
        #  todo: fix timescale to match units
        #       adjust power units
        t = data.timeList
        wind = np.array([0.0]*len(data.timeList))
        hydro = np.array([0.0]*len(data.timeList))
        pv = np.array([0.0]*len(data.timeList))

        for i in range(0, data.nDer):
            if data.derList[i].energy_type == 'Wind':
                wind += np.array(data.derList[i].output)
            if data.derList[i].energy_type == 'Hydro':
                hydro += np.array(data.derList[i].output)
            if data.derList[i].energy_type == 'PV':
                pv += np.array(data.derList[i].output)

        total = wind + hydro + pv

        if not np.all(wind == 0):
            canvas.axes.plot(t, wind, label="Wind Gen")
        if not np.all(hydro == 0):
            canvas.axes.plot(t, hydro, label="Hydro Gen")
        if not np.all(pv == 0):
            canvas.axes.plot(t, pv, label="Solar Gen")
        if np.all(total == 0):
            canvas.axes.plot(t, []*len(data.timeList), label="Total Renewable Gen")
        elif not np.all(total == 0):
            canvas.axes.plot(t, total, label="Total Renewable Gen")
        canvas.axes.legend(loc='upper left')
        canvas.axes.set_xlabel('Time (s)')
        canvas.axes.set_ylabel('Power Generation (MW)')
        canvas.axes.set_title('Time Plot of Renewable Power Gen.')
        canvas.draw()

    @staticmethod
    def renewable_stats(data):
        t = data.timeList

        # List of all generation types
        gen_types = []
        for i in range(data.nDer):
            if 'Storage' not in data.derList[i].energy_type:
                gen_types.append(data.derList[i].energy_type)

        gen_types = list(set(gen_types))

        # if no data found, return 0 for robustness
        if not gen_types:
            return 0

        num_gen = len(gen_types)
        gen_list = np.array([[0.0] * len(t) for j in range(num_gen)])

        for i in range(num_gen):
            # temp variable to hold total gen of one type
            temp_gen = np.array([0.0] * len(t))
            for x in range(data.nDer):
                if data.derList[x].energy_type == gen_types[i]:
                    temp_gen += np.array(data.derList[x].output)
                gen_list[i] = temp_gen

        total_gen_list = [0]*num_gen

        for i in range(num_gen):
            total_gen_list[i] = sum(gen_list[i])
            # convert to MWh

            total_gen_list[i] /= (len(t)*60*60)

        total_ren = 0
        total = 0
        for i in range(num_gen):
            total += total_gen_list[i]
            if 'Ren' in gen_types[i]:
                total_ren += total_gen_list[i]

        labels = []
        for i in range(num_gen):
            if 'Fuel' in gen_types[i]:
                labels.append(gen_types[i][5:] + ' (MWh)')
            elif 'Ren' in gen_types[i]:
                labels.append(gen_types[i][4:] + ' (MWh)')
        labels.append('Renewable (MWh)')
        labels.append('Total (MWh)')

        stats = []
        for i in range(num_gen):
            total_gen_list[i] = "%.2f" % total_gen_list[i]
            stats.append(total_gen_list[i])

        total_ren = "%.2f" % total_ren
        stats.append(total_ren)
        total = "%.2f" % total
        stats.append(total)

        return num_gen, stats, labels


