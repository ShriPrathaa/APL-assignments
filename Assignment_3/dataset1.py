import csv
import numpy as np
import matplotlib.pyplot as plt
x=[]            #initialisation of x
y=[]            #initialisation of y
with open("dataset1.txt", "r") as file:
    data = csv.reader(file,delimiter=' ')
    for row in data:    #reads each line into x,y
        x.append(float(row[0]))
        y.append(float(row[1]))
x=np.array(x)
y=np.array(y)
M = np.column_stack([x, np.ones(len(x))])   #construction of M matrix
(p1, p2), _, _, _ = np.linalg.lstsq(M, y, rcond=None)   #least square fitting
print(f"The estimated equation is {p1} x + {p2}")
y1=[p1*i+p2 for i in x]                     # estimated values
noise=(y1-y)                                #noise extraction
plt.plot(x,y)                               #plotting original data
plt.plot(x,y1)                              #plotting estimated data
plt.errorbar(x[::25], y[::25], np.std(noise), fmt='r.')
plt.legend(["Noisy","Estimated","Errorbar"],loc='upper left')
plt.savefig("dataset1.png")
