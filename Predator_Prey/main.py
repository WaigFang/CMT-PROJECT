import numpy as np
import math as m
import matplotlib.pyplot as plt
import csv
import ctypes
import os
import sys
from pathlib import Path
import pandas as pd
from scipy.integrate import odeint

lib_path = Path(sys.path[0]).parent
fonc = ctypes.CDLL(lib_path.joinpath("bin","clib.so"))



fonc.prey_growth_rate.argtypes = (ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double)
fonc.prey_growth_rate.restype = ctypes.c_double

fonc.predator_growth_rate.argtypes = (ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double)
fonc.predator_growth_rate.restype = ctypes.c_double

fonc.simulate_lotka_volterra.argtypes = [
   ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, 
    ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, 
    ctypes.c_char_p,ctypes.c_char_p
 ]

fonc.simulate_lotka_volterra.restype = None

class Timepopulation(ctypes.Structure):
    _fields_ = [
        ("t", ctypes.POINTER(ctypes.c_double)),
        ("x", ctypes.POINTER(ctypes.c_double)),
        ("y", ctypes.POINTER(ctypes.c_double))
    ]
fonc.population_evolution.restype = ctypes.POINTER(Timepopulation)
fonc.population_evolution.argtypes = [
    ctypes.c_int,  
    ctypes.c_double,  
    ctypes.c_double,  
    ctypes.c_double,  
    ctypes.c_double,  
    ctypes.c_double, 
    ctypes.c_double   
]
fonc.free_population.argtypes = [ctypes.POINTER(Timepopulation)]
fonc.free_population.restype = None


Leigh = pd.read_csv("Data/Leigh1968_harelynx.csv") 
plt.plot(Leigh["Time"],Leigh["Prey"],label="Prey")
plt.plot(Leigh["Time"],Leigh["Predator"],label="Predator")
plt.title("Hare and Lynx Population over Time")
plt.xlabel("Time")
plt.ylabel("Population")
plt.legend()
# plt.savefig("Outputs/Hare_and_Lynx_Populations.png")
plt.show()

a = 0.7 
b = 0.5
d = 0.2 
g = 0.3
x0 = 1.0 
y0 = 2.0  


#call the fonction 
fonc.simulate_lotka_volterra(a, b, d, g, x0, y0,100.0,1.0,b"Outputs/lotka_volterra_data.csv",b"Outputs/dx_dy_data.csv") # alpha,beta,gamma,delta,x0,y0,max time,dt,file name 
# a = 1 , b = 0.2 , d = 0.5 , g = 0.2 with x=1 y=2 works also for x=y=2

# Load the data into Python
data = pd.read_csv("Outputs/lotka_volterra_data.csv")

# Plot the results
plt.plot(data["Time"], data["Prey"], label="Prey")
plt.plot(data["Time"], data["Predator"], label="Predator")
plt.xlabel("Time")
plt.ylabel("Population")
plt.title("Lotka-Volterra Simulation of Prey and Predator Population over Time")
plt.legend()
# plt.savefig("Outputs/Lotka_Volterra_Simulation.png")
plt.show()


#here we get the solution but we want to be able to find a  way of using C 
def simulate_lotka_volterra(u, t, a, b, d, g):
    x, y = u  # x is prey (hares), y is predator (lynx)
    dxdt =fonc.prey_growth_rate(a,b,x,y)# Prey growth and predation
    dydt =fonc.predator_growth_rate(d,g,x,y)# Predator reproduction and death
    return [dxdt, dydt]


initial_conditions = [x0, y0]
t = np.linspace(0, 100, 1000)
solver = odeint(simulate_lotka_volterra,initial_conditions,t,args=(a, b, d, g))
prey = solver[:, 0]
predator = solver[:, 1]
plt.figure(figsize=(10, 6))
plt.plot(t, prey, label='Hare Population (Prey)', color='blue')
plt.plot(t, predator, label='Lynx Population (Predator)', color='red')
plt.title('Solutions of the Lotka-Volterra equation')
plt.xlabel('Time')
plt.ylabel('Population')
plt.legend()
# plt.savefig("Outputs/Lotka_Volterra_Solutions.png")
plt.show()

plt.plot(prey,predator,label="Population",color="blue")
plt.xlabel("Hare Population")
plt.ylabel("Lynx Population")
plt.title("Hare and Lynx Density")
plt.legend()
# plt.savefig("Outputs/Hare_and_Lynx_Density.png")
plt.show()

#otra prueba mas
# result = fonc.population_evolution(56,0.030484, 0.0000057, 0.103447, -0.000020, 21000, 49000)
# if not result:
#     raise MemoryError("Failed to allocate memory in C code.")

# # Extract data from the C struct
# time = np.ctypeslib.as_array(result.contents.t,shape=(56,))
# prey = np.ctypeslib.as_array(result.contents.x ,shape=(56,))
# predator = np.ctypeslib.as_array(result.contents.y,shape=(56,))
# print(time)
# print(prey)
# print(predator)
# fonc.free_population(result)
# plt.figure(figsize=(10, 6))
# plt.plot(time, prey, label="Prey Population")
# plt.plot(time, predator, label="Predator Population")
# plt.xlabel("Time")
# plt.ylabel("Population")
# plt.legend()
# plt.title("Population Evolution (Lotka-Volterra)")
# plt.grid()
# plt.show()


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