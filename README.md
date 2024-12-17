# CMT-PROJECT 

## Project description

Our program's aim is to study the population growth and change over time of a system consisting of predators and their's preys. Thanks to the Lotka-Volterra equations.

The program will:
1. Read Hare and lynx data found in "*Data/Leigh1968_harelynx.csv*",
2. Generate a table with dH and dL in "*Outputs/dx_dy_data.csv*", and of population in "*Outputs/Lotka_Volterra_Data.csv*",
3. Plot the population over time in "*Outputs/Lotka_Volterra_Simulation.png*",
4. Plot solutions over time in "*Outputs/Lotka_Volterra_Solutions.png*",
5. Plot population density in "*Outputs/Hare_and_Lynx_Density.png*",
6. (SENSIBILITY)

## Project structure
- "*Data/*" contains input data,
- "*Outputs/*" contains program outputs,
- "*Predator_Prey/*" contains program code,
- "*bin/*" contains the shared library between C and Python,
- "*Docs/*" contains a report discussing the results and the overall code,

### Inputs and Outputs

Inputs:
- "*Data/Leigh1968_harelynx.csv*" is a comma-separated file found as a table.
  
Outputs:
- "*Outputs/dx_dy_data.csv*" is a comma-separated file,
- "*Outputs/Lotka_Volterra_Data.csv*" is a comma-separated file,
- "*Outputs/Lotka_Volterra_Simulation.png*" is an image file,
- "*Outputs/Lotka_Volterra_Solutions.png*", is an image file,
- "*Outputs/Hare_and_Lynx_Density.png*" is an image file,
- (SENSIBILITY.png) is an image file. 

### Implementation details
Overview: 
- We used C as our main language, in which we created fuctions, to perform all of the needed calculations. This program is then compiled into a shared library called clib.so that will be used by Python via the `ctypes` module.
- Python handles most of the I/O, this includes reading csv files and then outputing tables and plots.

Structure in the directory "*Predator_Prey/*":
- "*Fonctions.c*":
  - contains the majority of coded functions used in our simulation,
  - is exported as "*bin/clib.so*" as a module,
- "*main.py*":
  - imports "*bin/clib.so*" as a module
  - reads in "*Data/Leigh1968_harelynx.csv*" and makes a plot,
  - uses all of functions provieded by "*clib.so*" to find the solution to the 
    Lotka-Volterra equations and plots them,

(FALTA ALGO AQUI CREO PERO NO SE QUE ES PROJECT ROOT DIRECTORY IS ASSIGNED USING ?) 


## Instructions

To reproduce results in the report, 2 steps should be followed: 
1. Compile the shared library,
2. Run the program,

EXPLAIN 

## Requirements

We provide the versions of Python and C that were used for this program: 
[ask in VSCODE AND COPY]
python = 3.12.4
gcc = 13.2.0 

You can also see more precisely the requirements in "*requirements.txt*" file for Python modules. This file was generated with the command: 
```{sh}
conda list --export > requirements.txt
```
## Possible Uses of The Program 

The program could be used to analyze predator-prey dynamics in different ecosystems. Helping in the design of conservation strategies, such as estimating the impact of predator culling or prey population boosting. 
Parameter values (such as $$\beta$$ ) could reveal insights into the stability or imbalance of the ecosystems. 
Once those parameters are estimated, we could use them to predict future population trends for both species.




## Credits
LEO WAIG FANG HERNANDEZ and MARCO MARINO    
