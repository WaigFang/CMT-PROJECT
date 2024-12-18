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

#create a function to be accesible by odeint / could be possible to right this same function on C and see if it works -> To do list
def simulate_lotka_volterra(u, t, a, b, d, g):
    x, y = u  # x is prey (hares), y is predator (lynx)
    dxdt =func.prey_growth_rate(a,b,x,y)# Prey growth and predation
    dydt =func.predator_growth_rate(d,g,x,y)# Predator reproduction and death
    return [dxdt, dydt]

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
# changed the value from 10 to 30 to get more more values => to get a more smooth plot 
a_values = np.linspace(0.75, 1.25, 30)
b_values = np.linspace(0.15, 0.25, 30) 
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


results_prey = []
results_predator = []
alpha_values = []
beta_values = []

t2 = np.linspace(0, 50, 200) 
for a in a_values:
    for b in b_values:
        solver = odeint(simulate_lotka_volterra, initial_conditions, t2, args=(a, b, d, g))
        prey = solver[:, 0]
        predator = solver[:, 1]
        results_prey.append(prey)
        results_predator.append(predator)
        alpha_values.append(a)
        beta_values.append(b)

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
plt.fill_between(t2, data_prey.max(axis=1), color="lightblue", alpha=0.3, label="Max-Min")
plt.fill_between(t2, mean_prey - std_prey, mean_prey + std_prey, color="blue", alpha=0.3, label="Mean ± SD")
plt.plot(t2, mean_prey, color="blue", label="Mean")
plt.title("Prey")
plt.xlabel("Time")
plt.ylabel("Density Population")
plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5))

plt.subplot(1, 2, 2)
plt.fill_between(t2, data_predator.max(axis=1), color="lightcoral", alpha=0.3, label="Max-Min")
plt.fill_between(t2, mean_predator - std_predator, mean_predator + std_predator, color="red", alpha=0.3, label="Mean ± SD")
plt.plot(t2, mean_predator, color="red", label="Mean")
plt.title("Predator")
plt.xlabel("Time")
plt.ylabel("Density Population")
plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5))

plt.suptitle("Sensitivity to alpha and beta", fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
#plt.savefig("Outputs/Sensitivity_Test.png")
plt.show()



# Transform the data frame from wide to long format
data_prey_long = data_prey.melt(var_name='simulation', value_name='abundance')
data_predator_long = data_predator.melt(var_name='simulation', value_name='abundance')

# Add time and species columns
data_prey_long['time'] = np.tile(t2, len(data_prey.columns))
data_prey_long['species'] = 'Prey'
data_predator_long['time'] = np.tile(t2, len(data_predator.columns))
data_predator_long['species'] = 'Predator'

# Combine prey and predator data frames
data_long = pd.concat([data_prey_long, data_predator_long], ignore_index=True)

# Add alpha and beta columns
num_simulations = len(a_values) * len(b_values)
data_long['alpha'] = np.repeat(alpha_values, len(t2))
data_long['beta'] = np.repeat(beta_values, len(t2))

# Summarize the data to calculate the envelopes
summary_data = data_long.groupby(['species', 'time']).agg(
    a_mean=('abundance', 'mean'),
    a_min=('abundance', 'min'),
    a_max=('abundance', 'max'),
    a_sd=('abundance', 'std')
).reset_index()

summary_data['a_psd'] = summary_data['a_mean'] + summary_data['a_sd']
summary_data['a_msd'] = summary_data['a_mean'] - summary_data['a_sd']

# Plot the results with mean ± sd
plt.figure(figsize=(14, 6))

for species in ['Prey', 'Predator']:
    species_data = summary_data[summary_data['species'] == species]
    plt.fill_between(species_data['time'], species_data['a_msd'], species_data['a_psd'], alpha=0.2)
    plt.plot(species_data['time'], species_data['a_mean'], label=f'Mean {species} Population')

plt.title("Sensitivity to alpha and beta (mean ± sd)")
plt.xlabel("Time")
plt.ylabel("Population density")
plt.legend(loc='center left', bbox_to_anchor=(1.05, 0.5))
plt.show()



















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