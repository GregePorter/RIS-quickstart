import numpy 
import os
print(os.environ['HOME'])
print(os.environ)

array = numpy.array([[2, 4, 6], 
                 [8, 10, 12], 
                 [14, 16, 18]]) 
numpy.savetxt("even.csv", array, delimiter = ",")
