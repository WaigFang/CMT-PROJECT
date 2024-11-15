import numpy as np
import math as m
import matplotlib.pyplot as plt
import csv


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
plt.title("Populations of Hares and Lynxs in function of time")
plt.xlabel("Time (Years)")
plt.ylabel("Population")
plt.plot(Years,Lynxs, label="Lynx Population")
plt.plot(Years,Hares, label ="Hare Popuation")
plt.legend()
plt.show()
#Plots both populations in function of time 

