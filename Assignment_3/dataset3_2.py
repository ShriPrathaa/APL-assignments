import numpy as np
import csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
f = []
y1 = []
with open("dataset3.txt", "r") as file:
    data = csv.reader(file, delimiter=' ')
    for row in data:        #reading data
        f.append(float(row[0]))
        y1.append(float(row[1]))
def plank(f, T1,h,c1):      #radiation intensity function
    return [(2 * h * (x**3) / ((c1) * np.exp((h * x / (T1)))-1)) for x in f]
sp1, _ = curve_fit(plank, f, y1, bounds=([4e-20, 3.25e-34, 8e16], [1e-19, 1e-33, 1e17]),method='trf') 
#curve fitting after changing algorithm
y2 = np.array(plank(f, sp1[0],sp1[1],sp1[2]))  #estimated values
print(f"h= {sp1[1]}\nc= {np.sqrt(sp1[2])}")
kB = 1.3806452e-23 
T=sp1[0]/kB
print(f"T= {T:.3f}\nkB= {kB}")
plt.plot(f, y1,f,y2)                                  #plotting
plt.legend(["Original","Estimated"])
plt.savefig("dataset3_2.png")
