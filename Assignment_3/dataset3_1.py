import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
kB = 1.3806452e-23      #constant parameters
h = 6.62607015e-34
c = 299792458
f = []
y1 = []
with open("dataset3.txt", "r") as file:
    data = csv.reader(file, delimiter=' ')
    for row in data:  #reading data
        f.append(float(row[0]))
        y1.append(float(row[1]))
f=np.array(f)
y1=np.array(y1)
def plank(f, T):    #radiation intensity function
    return (2 * h * (f**3) / ((c**2) * np.exp((h * f / (kB * T)))-1))
guess = 1e5        #initial guess
sp1, _ = curve_fit(plank, f, y1,guess) #curve fitting
print(f"{sp1}")
y2 = plank(f, sp1)          #estimated values
plt.plot(f, y1,f,y2)             #plotting
plt.legend(["Original","Estimated"])
plt.savefig("dataset3_1.png")
