import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
def period(t,y):
    m=-np.inf
    maxy=(max(y))
    find=0
    ini = 0  # Initialize the start index
    end = 0  # Initialize the end index
    for i in range(len(y)):
        if(find==0):
            if(abs(y[i]-maxy)<=0.5 and y[i]>y[i - 1] and y[i+1]<y[i]):
                m=y[i]
                ini=i       #finding first maximum
                find=1      
        elif(find==1):
            if abs(y[i]+m)<0.001:
                end=i       #finding first minimum, negative of 1st maximum
                break
    return 2*(t[end]-t[ini])
t=[]            #initialisation of t
fnc=[]          #initialisation of fnc
with open("dataset2.txt", "r") as file:
    data = csv.reader(file,delimiter=' ')
    for row in data:    #reading each line
        t.append(float(row[0]))
        fnc.append(float(row[1]))
t=np.array(t)
fnc=np.array(fnc)
T=period(t,fnc)         #finding time period
print(f"The time period is {T}")
t1=(2*np.pi *t/T)
for c in range(3,20,2):
    M1 = np.column_stack([np.sin(t1),np.sin(3*t1),np.sin(c*t1)]) #forming M matrix
    p, _, _, _ = np.linalg.lstsq(M1, fnc, rcond=None)            #least square fit   
    fnc1=p[0]*np.sin(t1)+p[1]*np.sin(3*t1)+p[2]*np.sin(c*t1) 
    n=(fnc1-fnc)
    if(np.std(n)<=0.6):  #ideal frequencies have std of about 0.5, others around 0.9
        break
af=2*np.pi/T
print(f"""The estimated parameters are: {p[0]} sin(t*{af}) 
      +{p[1]} sin(t*{3*af}) +{p[2]} sin(t*{c*af})""")
plt.plot(t,fnc,t,fnc1)
plt.legend(["Original","Estimated from lstsq"])
plt.savefig("dataset2_lstsq.png")
print(f"The standard deviation in using  is np.linalg.lstsq is {np.std(n)}")
def sinfunc(t, p1, p2,p3,c,b):
    return p1* np.sin(b*t1)+p2*np.sin(3*b*t1)+p3* np.sin(c*t1) 
guess=[10,2,3,5,1]
(sp1, sp2,sp3,c1,b1), _ = curve_fit(sinfunc, t, fnc, guess)
print(f"""The estimated parameters are: {sp1} sin(t*{b1*af}) +
       {sp2} sin(t*{3*b1*af})+{sp3} sin(t*{c1*af})""")
sest = sinfunc(t, sp1, sp2,sp3,c1,b1)   # Regenerate data
plt.plot(t, fnc, t, sest)
plt.legend(["Original","Estimated from curvefit"])
plt.savefig("dataset2_curvefit.png")
n=[(sest[i]-fnc[i]) for i in range(len(sest))]
print(f"The standard deviation in using scipy.optimize.curve_fit() is {np.std(n)}")
