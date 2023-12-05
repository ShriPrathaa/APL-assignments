import csv
import matplotlib.pyplot as plt
import numpy as np
criteria = {}                 # Initialize an empty dictionary to store the criteria data
with open("ass4.csv", "r") as file:
    data = csv.reader(file)   # Open the CSV file for reading
    header = next(data)       # Read header row for keys in the dictionary
    for key in header:
        criteria[key] = []    # Initialize each key with an empty list
    for row in data:          # Read and process the remaining rows
        for key, value in zip(header, row):
            criteria[key].append( float(value))
select = header[1:8]          #selecting the factors affecting chance
array = np.full(500, 6)
array=np.array(criteria[header[3]])/5
a1=np.array(criteria[select[0]])/340
a2=np.array(criteria[select[1]])/120
a4=np.array(criteria[select[3]])/5
a5=np.array(criteria[select[4]])/5
a6=np.array(criteria[select[5]])/10
a7=np.full(500,1)
print("Factors affecting chance:\n",select)    
M = np.column_stack((a1,a2,array,a4,a5,a6,criteria[select[6]],a7))     # Create matrix M
p1, _, _, _ = np.linalg.lstsq(M, criteria[header[-1]], rcond=None)
y = np.zeros(len(criteria[select[0]]))
for i in range(len(p1)):
    y = (p1[0] * a1 +p1[1] * a2 +p1[2] * array +p1[3] * a4 +p1[4] * a5 +p1[5] * a6 +p1[6] * np.array(criteria[select[6]]) +p1[7] * a7)
y2=np.array(criteria[header[-1]])
print("Standard deviation in using least squares:\n",np.std(y2-y))
print("Coefficients of factors:\n",p1)
plt.scatter(criteria[header[0]],y,c='cyan')
plt.scatter(criteria[header[0]],criteria[header[-1]],marker='*',c='blue')
plt.savefig("lstsq.png")
plt.figure()
plt.scatter(criteria[header[1]],criteria[header[-1]],c='red')
plt.scatter(criteria[header[1]],y,marker='*',c='pink')
plt.savefig("GRE.png")
plt.figure()
plt.scatter(criteria[header[2]],criteria[header[-1]],c='red')
plt.scatter(criteria[header[2]],y,marker='*',c='pink')
plt.savefig("TOEFL.png")
plt.figure()
plt.scatter(criteria[header[3]],criteria[header[-1]],c='purple')
plt.scatter(criteria[header[3]],y,marker='*')
plt.savefig("Univ_Rank.png")
plt.figure()
plt.scatter(criteria[header[4]],criteria[header[-1]],c='purple')
plt.scatter(criteria[header[4]],y,marker='*')
plt.savefig("SOP.png")
plt.figure()
plt.scatter(criteria[header[5]],criteria[header[-1]],c='red')
plt.scatter(criteria[header[5]],y,marker='*',c='orange')
plt.savefig("LOR.png")
plt.figure()
plt.scatter(criteria[header[6]],criteria[header[-1]],c='red')
plt.scatter(criteria[header[6]],y,marker='*',c='orange')
plt.savefig("CGPA.png")
plt.figure()
plt.scatter(criteria[header[7]],criteria[header[-1]],c='magenta')
plt.scatter(criteria[header[7]],y,marker='*',c='violet')
plt.savefig("research.png")
plt.figure()
a1=(np.array(criteria[select[0]])/340)**0.6
a2=(np.array(criteria[select[1]])/120)**0.4
a6=(np.array(criteria[select[5]])/10)**2
M = np.column_stack((a1,a2,array,a4,a5,a6,criteria[select[6]],a7))     # Create matrix M
p1, _, _, _ = np.linalg.lstsq(M, criteria[header[-1]], rcond=None)
y = np.zeros(len(criteria[select[0]]))
for i in range(len(p1)):
    y = (p1[0] * a1 +p1[1] * a2 +p1[2] * array +p1[3] * a4 +p1[4] * a5 +p1[5] * a6 +p1[6] * np.array(criteria[select[6]]) +p1[7] * a7)
y2=np.array(criteria[header[-1]])
print("Standard deviation in using non linear relations:\n",np.std(y2-y))
print("Coefficients of factors:\n",p1)
