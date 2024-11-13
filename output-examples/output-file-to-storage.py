import numpy
import os

print(os.environ['STORAGE'])

array = numpy.array([[2, 4, 6],
                     [8, 10, 12],
                      [14, 16, 18]])

numpy.savetxt(os.environ['STORAGE']+"/even.csv", array, delimiter = ",")
