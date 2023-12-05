import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import warnings
warnings.filterwarnings("ignore")
lnall = None
lngood = None
bestx=0
bestcost=0
def generic_gradient_descent(frames, f, df, x_range, learning_rate, num_steps):
    global xall, yall, lnall, lngood,bestx,bestcost
    xall = []  # Initialize xall as an empty list before the animation
    yall = []  # Initialize yall as an empty list before the animation
    for _ in range(num_steps):
        x = bestx - df(bestx) * learning_rate
        bestx = x
        bestcost = f(bestx)
        xall.append(bestx)
        yall.append(bestcost)
        lnall.set_data(xall, yall)
        lngood.set_data([bestx], [bestcost])

def gradient_descent(frames, f, df_dx, df_dy, bestx, besty, lr, num_steps):
    global xall, yall, zall, lnall, lngood
    xall.append(bestx)
    yall.append(besty)
    zall.append(f(bestx, besty))
    lnall.set_data(xall, yall)
    lnall.set_3d_properties(zall)
    for _ in range(num_steps):
        x = bestx - df_dx(bestx, besty) * lr
        y = besty - df_dy(bestx, besty) * lr
        bestx = x
        besty = y
        z = f(x, y)
        bestcost=z
        xall.append(x)
        yall.append(y)
        zall.append(z)
        lnall.set_data(xall, yall)
        lnall.set_3d_properties(zall)
        lngood.set_data([bestx], [besty])
        lngood.set_3d_properties([bestcost])
    
#function definitions
def f1(x):
    return x ** 2 + 3 * x + 8
def df1(x):
    return 2 * x + 3
def f3(x, y):
    return x**4 - 16*x**3 + 96*x**2 - 256*x + y**2 - 4*y + 262
def df3_dx(x, y):
    return 4*x**3 - 48*x**2 + 192*x - 256
def df3_dy(x, y):
    return 2*y - 4
def f4(x,y):
    return np.exp(-(x - y)**2) * np.sin(y)
def df4_dx(x, y):
    return -2 * np.exp(-(x - y)**2) * np.sin(y) * (x - y)
def df4_dy(x, y):
    return np.exp(-(x - y)**2) * np.cos(y) + 2 * np.exp(-(x - y)**2) * np.sin(y)*(x - y)
def f5(x):
    return np.cos(x)**4 - np.sin(x)**3 - 4*np.sin(x)**2 + np.cos(x) + 1
def f5d(x):
    return -4*np.cos(x)**3*np.sin(x) -3* np.sin(x)**2*np.cos(x) - 8*np.sin(x)*np.cos(x) - np.sin(x)
global learning_rate
xbase = np.linspace(-5, 5, 500)  #x values
ybase = f1(xbase)                #y values
bestx = 1.98                     # initial values
bestcost = f1(bestx)
x_range = (-5, 5)
learning_rate = 0.1              #learning rate
num_steps = 10                   #number of steps
fig, ax = plt.subplots()         #creating plots
ax.plot(xbase, ybase)
xall, yall = [], []
lnall, = ax.plot([], [], 'ro-') 
lngood, = ax.plot([], [], 'go', markersize=10)
ani= FuncAnimation(fig, generic_gradient_descent, frames=range(num_steps),fargs=(f1, df1, x_range, learning_rate, num_steps), interval=1000, repeat=False)
print(f"f1:")
ani.save("animation1.gif",writer='pillow')
plt.show()
print(f"Minima of function occurs at x={bestx} and is y={bestcost}")  # Print results after animation

xbase = np.linspace(-10, 10, 100)    #x values
ybase = np.linspace(-10, 10, 100)    #y values
x, y = np.meshgrid(xbase, ybase)
zbase = f3(x, y)                     #z values
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')#creating plots
ax.plot_surface(x, y, zbase, cmap='autumn', alpha=0.8, shade=True)
global besty, lr
bestx =5
besty = -2
xall, yall, zall = [], [], []
lnall, = ax.plot([], [], [], 'bo', markersize=2)
lngood, = ax.plot([], [], [], 'ro', color='black')
lr = 0.1                            #learning rate
num_steps = 10                      #number of steps
ani = FuncAnimation(fig, gradient_descent, frames=range(num_steps),fargs=(f3, df3_dx, df3_dy, bestx, besty, lr, num_steps), interval=1000, repeat=False)
print(f"f3:")
ani.save("animation2.gif",writer='pillow')
plt.show()
print(f"Minima of function occurs at x={xall[-1]},y={yall[-1]} and is z={zall[-1]}")

xbase = np.linspace(-np.pi, np.pi, 100)  #x values
ybase = np.linspace(-np.pi, np.pi, 100)  #y values
x, y = np.meshgrid(xbase, ybase)
zbase = f4(x, y)                        #z values
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')#creating plots
ax.plot_surface(x, y, zbase, cmap='autumn', alpha=0.8, shade=True)
bestx =0
besty = -1.5
xall, yall, zall = [], [], []
lnall, = ax.plot([], [], [], 'bo', markersize=4)
lngood, = ax.plot([], [], [], 'ro', color='black')
lr = 0.2                                   #learning rate
num_steps = 40                         #number of steps
ani = FuncAnimation(fig, gradient_descent, frames=range(num_steps),fargs=(f4, df4_dx, df4_dy, bestx,besty, lr, num_steps),interval=100, repeat=False)
ani.save("animation3.gif",writer='pillow')
print(f"f4")
plt.show()
print(f"Minima of function occurs at x={xall[-1]},y={yall[-1]} and is z={zall[-1]}")

xbase = np.linspace(0,2*np.pi, 500)#x values
ybase = f5(xbase) #y values
bestx = 3.1  #initial value
bestcost = f5(bestx)
x_range = (0,2*np.pi )
num_steps = 10    #number of steps
lr = 0.1             #learning rate
xall, yall = [], []
fig, ax = plt.subplots()
ax.plot(xbase, ybase)
lnall,  = ax.plot([], [], 'ro-')
lngood, = ax.plot([], [], 'go', markersize=10)
ani= FuncAnimation(fig, generic_gradient_descent, frames=range(10), fargs=(f5, f5d, x_range, lr, num_steps),interval=1000, repeat=False)
ani.save("animation4.gif",writer='pillow')
print(f"f5")
plt.show()
print(f"Minima of function occurs at x={bestx} and is y={bestcost}")  
