import numpy as np
import math as m
import matplotlib.pyplot as plt
import csv
import ctypes
import os
import sys
from pathlib import Path

lib_path = Path(sys.path[0]).parent
fonc = ctypes.CDLL(lib_path.joinpath("bin","clib.so"))



fonc.prey_growth_rate.argtypes = (ctypes.c_double,ctypes.c_double,ctypes.c_int,ctypes.c_int)
fonc.prey_growth_rate.restype = ctypes.c_double

fonc.predator_growth_rate.argtypes = (ctypes.c_double,ctypes.c_double,ctypes.c_int,ctypes.c_int)
fonc.predator_growth_rate.restype = ctypes.c_double


class Timepopulation(ctypes.Structure):
    _fields_ = [
        ("t", ctypes.POINTER(ctypes.c_double)),
        ("x", ctypes.POINTER(ctypes.c_double)),
        ("y", ctypes.POINTER(ctypes.c_double))
    ]
fonc.population_evolution.restype = ctypes.POINTER(Timepopulation)
fonc.population_evolution.argtypes = [
    ctypes.c_int,  # maxtime
    ctypes.c_double,  # alpha
    ctypes.c_double,  # beta
    ctypes.c_double,  # delta
    ctypes.c_double,  # gamma
    ctypes.c_double,  # x
    ctypes.c_double   # y
]
fonc.free_population.argtypes = [ctypes.POINTER(Timepopulation)]
fonc.free_population.restype = None

file = open("Data/Leigh1968_harelynx.csv", "r")
csvReader = csv.reader(file, delimiter = ',')
Years = []
Hares = []
Lynxs = []
for row in csvReader: 
    Year = int(row[0])
    Years.append(Year)
    Hare = int(row[1])
    Hares.append(Hare)
    Lynx = int(row[2])
    Lynxs.append(Lynx)

# Reads the csv file and creates multiple lists with the data, this real data can be used to determine if our model is more or less realistic
plt.title("Population of Hares and Lynxs in function of time")
plt.xlabel("Time (Years)")
plt.ylabel("Population")
plt.plot(Years,Lynxs,label="Lynx Population",color="red")
plt.plot(Years,Hares,label="Hare Popuation",color="blue")
plt.legend()
plt.show()




#otra prueba mas
result = fonc.population_evolution(56, 0.4, 0.5, 0.09, 2.0, 21000, 49000)
if not result:
    raise MemoryError("Failed to allocate memory in C code.")

# Extract data from the C struct
# time = np.array([result.contents.t[i] for i in range(56)])
# prey = np.array([result.contents.x[i] for i in range(56)])
# predator = np.array([result.contents.y[i] for i in range(56)])
time = np.ctypeslib.as_array(result.contents.t, shape=(56,))
prey = np.ctypeslib.as_array(result.contents.x, shape=(56,))
predator = np.ctypeslib.as_array(result.contents.y, shape=(56,))
print(time)
print(prey)
print(predator)
fonc.free_population(result)
plt.figure(figsize=(10, 6))
plt.plot(time, prey, label="Prey Population")
plt.plot(time, predator, label="Predator Population")
plt.xlabel("Time")
plt.ylabel("Population")
plt.legend()
plt.title("Population Evolution (Lotka-Volterra)")
plt.grid()
plt.show()


#Plots both populations in function of time
# pruebas= []
# for i in range (len(Hares)):
#     prueba = fonc.prey_growth_rate(0.500,0.03,Hares[i],Lynxs[i])
#     pruebas.append(prueba)

# plt.plot(Years,pruebas)
# plt.title("Model Predicted Prey Growth Rate")
# plt.xlabel("Time (Years)")
# plt.ylabel("Predicted Prey Growth")
# plt.show() #look for errors as I do not understand what we are computing 