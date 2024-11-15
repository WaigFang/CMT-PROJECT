import numpy as np
import math as m
import matplotlib.pyplot as plt
import csv

file = open("Data/Leigh1968_harelynx.csv", "r")
csvReader = csv.reader(file, delimiter = ',')
print(type(csvReader))
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


