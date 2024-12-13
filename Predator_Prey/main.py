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


#Revise this to get actually what we want 
t_max = 100
dt = 1
# Define the new function for predator-prey dynamics
def prey_predator_dynamics(a, b, d, g, x, y, dt):
    dx = a * x - b * x * y  # Prey growth equation
    dy = d * x * y - g * y  # Predator growth equation
    return dx, dy

# Simulate the new predator-prey model over time
def simulate_preypredator_model(a, b, d, g, x0, y0, t_max, dt):
    times = np.arange(0, t_max, dt)
    prey_pop = np.zeros(len(times))
    predator_pop = np.zeros(len(times))
    
    # Initial conditions
    prey_pop[0] = x0
    predator_pop[0] = y0

    # Iterate over time steps
    for i in range(1, len(times)):
        dx, dy = prey_predator_dynamics(a, b, d, g, prey_pop[i-1], predator_pop[i-1], dt)
        prey_pop[i] = prey_pop[i-1] + dx * dt
        predator_pop[i] = predator_pop[i-1] + dy * dt
        
        # Ensure populations don't go negative
        prey_pop[i] = max(prey_pop[i], 0)
        predator_pop[i] = max(predator_pop[i], 0)
    
    return times, prey_pop, predator_pop

# Time range
times = np.linspace(0, 50, 1000)  # Time from 0 to 50, with 1000 time steps

# Parameter ranges
alpha_range = [0.75, 1.25]  # Range for 'a' (prey growth rate)
beta_range = [0.15, 0.25]  # Range for 'b' (predation rate)

# Create a grid of alpha and beta values
alpha_values = np.linspace(alpha_range[0], alpha_range[1], 5)  # 5 values for alpha
beta_values = np.linspace(beta_range[0], beta_range[1], 5)    # 5 values for beta

# Prepare storage for results
prey_results = []
predator_results = []

# Simulate for each combination of alpha and beta
for alpha in alpha_values:
    for beta in beta_values:
        times, prey_pop, predator_pop = simulate_preypredator_model(alpha, beta, d, g, x0, y0, t_max, dt)
        prey_results.append(prey_pop)
        predator_results.append(predator_pop)

# Convert results to arrays
prey_results = np.array(prey_results)
predator_results = np.array(predator_results)

# Calculate min, max, mean, and standard deviation
prey_min = np.min(prey_results, axis=0)
prey_max = np.max(prey_results, axis=0)
prey_mean = np.mean(prey_results, axis=0)
prey_std = np.std(prey_results, axis=0)

predator_min = np.min(predator_results, axis=0)
predator_max = np.max(predator_results, axis=0)
predator_mean = np.mean(predator_results, axis=0)
predator_std = np.std(predator_results, axis=0)

# Plotting
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

# Plot for Prey
ax1.fill_between(times, prey_min, prey_max, color='lightblue', alpha=0.4, label='Min-Max')
ax1.fill_between(times, prey_mean - prey_std, prey_mean + prey_std, color='skyblue', alpha=0.6, label='Mean ± SD')
ax1.plot(times, prey_mean, color='darkblue', linewidth=2, label='Mean')
ax1.set_title("Prey", fontsize=14, fontweight='bold')
ax1.set_xlabel("Time", fontsize=12)
ax1.set_ylabel("Population density", fontsize=12)
ax1.legend()

# Plot for Predator
ax2.fill_between(times, predator_min, predator_max, color='lightblue', alpha=0.4, label='Min-Max')
ax2.fill_between(times, predator_mean - predator_std, predator_mean + predator_std, color='skyblue', alpha=0.6, label='Mean ± SD')
ax2.plot(times, predator_mean, color='darkblue', linewidth=2, label='Mean')
ax2.set_title("Predator", fontsize=14, fontweight='bold')
ax2.set_xlabel("Time", fontsize=12)
ax2.set_ylabel("Population density", fontsize=12)
ax2.legend()

# Overall title
fig.suptitle("Sensitivity to alpha and beta", fontsize=16)

# Adjust layout
plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust for the overall title
plt.show()

#otra prueba mas
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