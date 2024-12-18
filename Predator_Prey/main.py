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
import seaborn as sns
import itertools

#locate the clib.so library 
lib_path = Path(sys.path[0]).parent 
func = ctypes.CDLL(lib_path.joinpath("bin","clib.so"))

#define what types of arguments and results are given by all functions in clib.so
func.prey_growth_rate.argtypes = (ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double)
func.prey_growth_rate.restype = ctypes.c_double

func.predator_growth_rate.argtypes = (ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double)
func.predator_growth_rate.restype = ctypes.c_double

func.simulate_lotka_volterra.argtypes = (ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_char_p,ctypes.c_char_p)
func.simulate_lotka_volterra.restype = None

func.sensitivity_test.argtypes = (ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_double,ctypes.c_char_p)
func.sensitivity_test.restype = None



#Reads the .csv and plot (pd.read_csv much faster than open etc...)
Leigh = pd.read_csv("Data/Leigh1968_harelynx.csv") 
plt.plot(Leigh["Time"],Leigh["Prey"],label="Prey")
plt.plot(Leigh["Time"],Leigh["Predator"],label="Predator")
plt.title("Hare and Lynx Population over Time")
plt.xlabel("Time")
plt.ylabel("Population")
plt.legend()
# plt.savefig("Outputs/Hare_and_Lynx_Populations.png")
plt.show()

#define parameters for equation 
a = 0.7 
b = 0.5
d = 0.2 
g = 0.3
x0 = 1.0 
y0 = 2.0  
initial_conditions = [x0, y0]
t = np.linspace(0, 100, 1000)

#call the function 
func.simulate_lotka_volterra(a, b, d, g, x0, y0,100.0,1.0,b"Outputs/lotka_volterra_data.csv",b"Outputs/dx_dy_data.csv") # alpha,beta,gamma,delta,x0,y0,max time,dt,file name 
# a = 1 , b = 0.2 , d = 0.5 , g = 0.2 with x=1 y=2 works also for x=y=2

#read
data = pd.read_csv("Outputs/lotka_volterra_data.csv")

# Plot the results over time 
plt.plot(data["Time"], data["Prey"], label="Prey")
plt.plot(data["Time"], data["Predator"], label="Predator")
plt.xlabel("Time")
plt.ylabel("Population")
plt.title("Lotka-Volterra Simulation of Prey and Predator Population over Time")
plt.legend()
# plt.savefig("Outputs/Lotka_Volterra_Simulation.png")
plt.show()


#create a function to be accesible by odeint / could be possible to right this same function on C and see if it works -> To do list
def simulate_lotka_volterra(u, t, a, b, d, g):
    x, y = u  # x is prey (hares), y is predator (lynx)
    dxdt =func.prey_growth_rate(a,b,x,y)# Prey growth and predation
    dydt =func.predator_growth_rate(d,g,x,y)# Predator reproduction and death
    return [dxdt, dydt]
#solve the equation with odeint
solver = odeint(simulate_lotka_volterra,initial_conditions,t,args=(a, b, d, g))
prey = solver[:, 0]
predator = solver[:, 1]
#plot results over time 
plt.figure(figsize=(10, 6))
plt.plot(t, prey, label='Hare Population (Prey)', color='blue')
plt.plot(t, predator, label='Lynx Population (Predator)', color='red')
plt.title('Solutions of the Lotka-Volterra equation')
plt.xlabel('Time')
plt.ylabel('Population')
plt.legend()
# plt.savefig("Outputs/Lotka_Volterra_Solutions.png")
plt.show()
#plot pop density 
plt.plot(prey,predator,label="Population",color="blue")
plt.xlabel("Hare Population")
plt.ylabel("Lynx Population")
plt.title("Hare and Lynx Density")
plt.legend()
# plt.savefig("Outputs/Hare_and_Lynx_Density.png")
plt.show()



a_values = np.linspace(0.75, 1.25, 10)  # Range of a values
b_values = np.linspace(0.15, 0.25, 10)  # Range of b values
# Perform the sensitivity test
# Perform the sensitivity test
results_prey = []
results_predator = []
t = np.linspace(0, 50, 200)  # Time points
for a in a_values:
    for b in b_values:
        solver = odeint(simulate_lotka_volterra, initial_conditions, t, args=(a, b, d, g))
        prey = solver[:, 0]
        predator = solver[:, 1]
        results_prey.append(prey)
        results_predator.append(predator)

# Convert results to a DataFrame for analysis and plotting
data_prey = pd.DataFrame(results_prey).T
data_predator = pd.DataFrame(results_predator).T

# Calculate mean and standard deviation for prey and predator populations
mean_prey = data_prey.mean(axis=1)
std_prey = data_prey.std(axis=1)
mean_predator = data_predator.mean(axis=1)
std_predator = data_predator.std(axis=1)

# Plot filled plot of the max a and max b and also mean ± sd
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.fill_between(t, data_prey.max(axis=1), color="lightblue", alpha=0.3, label="Max-Min")
plt.fill_between(t, mean_prey - std_prey, mean_prey + std_prey, color="blue", alpha=0.3, label="Mean ± SD Prey Population")
plt.plot(t, mean_prey, color="blue", label="Mean")
plt.title("Prey")
plt.xlabel("Time")
plt.ylabel("Density Population")
plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5))

plt.subplot(1, 2, 2)
plt.fill_between(t, data_predator.max(axis=1), color="lightcoral", alpha=0.3, label="Max-Min")
plt.fill_between(t, mean_predator - std_predator, mean_predator + std_predator, color="red", alpha=0.3, label="Mean ± SD Predator Population")
plt.plot(t, mean_predator, color="red", label="Mean")
plt.title("Predator")
plt.xlabel("Time")
plt.ylabel("Density Population")
plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5))

plt.suptitle("Sensitivity to alpha and beta", fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
























# func.sensitivity_test(0.75,1.5,0.15,0.25,0.5,0.2,1,2,100,1,b"Outputs/Sensitivity_test.csv")

# # Example 1: Heatmap for average predator population vs Alpha and Beta
# dataset = pd.read_csv("Outputs/Sensitivity_test.csv")
# heatmap_data = data.groupby(['Alpha', 'Beta']).mean().reset_index()
# heatmap_pivot = heatmap_data.pivot("Alpha", "Beta", "Predator")
# plt.figure(figsize=(10, 8))
# sns.heatmap(heatmap_pivot, cmap="coolwarm", annot=False, cbar_kws={'label': 'Avg Predator Population'})
# plt.title("Average Predator Population Sensitivity to Alpha and Beta")
# plt.xlabel("Beta")
# plt.ylabel("Alpha")
# plt.show()

# # Example 2: Line plots of prey and predator population over time for a specific Alpha, Beta pair
# alpha_value = 1.0  # Example value
# beta_value = 0.2   # Example value

# subset = data[(data['Alpha'] == alpha_value) & (data['Beta'] == beta_value)]

# plt.figure(figsize=(10, 6))
# plt.plot(subset['Time'], subset['Prey'], label="Prey Population", color="blue")
# plt.plot(subset['Time'], subset['Predator'], label="Predator Population", color="red")
# plt.title(f"Population Dynamics (Alpha={alpha_value}, Beta={beta_value})")
# plt.xlabel("Time")
# plt.ylabel("Population")
# plt.legend()
# plt.show()

# result = func.population_evolution(56,0.030484, 0.0000057, 0.103447, -0.000020, 21000, 49000)
# if not result:
#     raise MemoryError("Failed to allocate memory in C code.")

# # Extract data from the C struct
# time = np.ctypeslib.as_array(result.contents.t,shape=(56,))
# prey = np.ctypeslib.as_array(result.contents.x ,shape=(56,))
# predator = np.ctypeslib.as_array(result.contents.y,shape=(56,))
# print(time)
# print(prey)
# print(predator)
# func.free_population(result)
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
#     prueba = func.prey_growth_rate(0.500,0.03,Hares[i],Lynxs[i])
#     pruebas.append(prueba)

# plt.plot(Years,pruebas)
# plt.title("Model Predicted Prey Growth Rate")
# plt.xlabel("Time (Years)")
# plt.ylabel("Predicted Prey Growth")
# plt.show() #look for errors as I do not understand what we are computing 