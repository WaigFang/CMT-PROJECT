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
#Plots both populations in function of time
pruebas= []
for i in range (len(Hares)):
    prueba = fonc.prey_growth_rate(0.500,0.03,Hares[i],Lynxs[i])
    pruebas.append(prueba)

plt.plot(Years,pruebas)
plt.title("Model Predicted Prey Growth Rate")
plt.xlabel("Time (Years)")
plt.ylabel("Predicted Prey Growth")
plt.show() #look for errors as I do not understand what we are computing 