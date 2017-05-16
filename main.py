# def read_values(f):
#     string = f.readline()
#     string = string.split(' ')
#     string.pop()
#
#     for i in range(len(string)):
#         string[i] = float(string[i])
#     return string
#
#
# f = open('template.txt', 'r', 1)
#
#
#
#
# for i in range(7):
#     f.readline()
# f.read(8)
#
# voltage = read_values(f)
# print(voltage)

import data

Data = data.Data('sample.txt')

print(Data.timeList)
