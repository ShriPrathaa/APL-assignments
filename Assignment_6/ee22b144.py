import numpy as np
import matplotlib.pyplot as plt
import csv
import timeit
def distcost(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def distance(cities, cityorder):
    total_distance = 0
    N = len(cityorder)
    for i in range(N):
        current_city = cityorder[i]
        next_city = cityorder[(i + 1)%N]
        x1, y1 = cities[current_city]
        x2, y2 = cities[next_city]
        total_distance += distcost(x1, y1, x2, y2)
    return total_distance

def sim_anneal(cities,finalorder):
    T = 3
    decayrate = 0.8
    x=T
    bestcost=distance(cities,finalorder)
    N = len(finalorder)
    for i in range(N):
        for j in range(N-1,-1,-1):
            if i != j:  # Exclude cases where i is equal to j
                iter = finalorder.copy()  # Make a copy of finalorder to avoid modifying it
                iter[i] = finalorder[j]
                iter[j] = finalorder[i]
                present = distance(cities,iter)
                T = T * decayrate
                if present < bestcost:
                    bestcost = present
                    finalorder = iter
                elif np.exp(-(present-bestcost)/T)>np.random.random_sample() and (present-bestcost)<0.3:
                    bestcost = present
                    finalorder = iter
                if(T<x*decayrate**(N**3)):
                    break
    return finalorder,bestcost

# Rest of the code remains the same

def find_nearest_city(current_city, unvisited_cities, x, y):
    min_distance = float('inf')
    nearest_city = None

    for city in unvisited_cities:
        distance = distcost(x[current_city], y[current_city], x[city], y[city])
        if distance < min_distance:
            min_distance = distance
            nearest_city = city

    return nearest_city, min_distance

def tsp_selection_sort(x, y):
    num_cities = len(x)
    unvisited_cities = list(range(1, num_cities))
    tour = [0]
    total_distance = 0.0

    for _ in range(num_cities - 1):
        nearest_city, distance = find_nearest_city(tour[-1], unvisited_cities, x, y)
        tour.append(nearest_city)
        total_distance += distance
        unvisited_cities.remove(nearest_city)

    total_distance += distcost(x[tour[-2]], y[tour[-2]], x[0], y[0])

    return tour, total_distance

def plot(cities, cityorder):
    # Extract the city coordinates in the specified order
    xplot = [cities[i][0] for i in cityorder]
    yplot = [cities[i][1] for i in cityorder]
    
    # Close the loop for plotting by appending the coordinates of the first city at the end
    xplot.append(xplot[0])
    yplot.append(yplot[0])
    
    # Plot the cities
    plt.clf()
    plt.plot(xplot, yplot, 'o-')
    plt.show()
    print("Order:",cityorder)

def tsp(cities):
    N = len(cities)
    x_cities = [cities[i][0] for i in range(N)]
    y_cities = [cities[i][1] for i in range(N)]
    
    cityorder = np.arange(N)
    np.random.shuffle(cityorder)
    
    finalorder,cost1 = sim_anneal(cities, cityorder)
    tour, total_distance = tsp_selection_sort(x_cities, y_cities)

    # Calculate the cost using the distance function
    cost = distance(cities, cityorder)
    print(f"Initial distance = {cost}")
    plot(cities,cityorder)
    plot(cities,finalorder)
    print("Distance after simulated annealing:\n",cost1)
    print("Percentage improvement after simulated annealing:\n",(cost-cost1)*100/cost)
    plot(cities,tour)
    print("Distance after selection sort:\n",total_distance)
    print("Percentage improvement after selection sort:\n",(cost-total_distance)*100/cost)
    if(cost1<total_distance ):
        return finalorder
    return tour

with open("C:\\Users\\shrip\\Downloads\\tsp40.txt", 'r') as f:
    reader = csv.reader(f, delimiter=' ')
    cities = []

    # Read city coordinates from the CSV file
    for i, row in enumerate(reader):
        if i == 0:
            # Define the number of cities
            N = int(row[0])
        elif i <= N:
            # Append city coordinates as a tuple to the 'cities' list
            cities.append((float(row[0]), float(row[1])))
def time():  
    order=tsp(cities)
print(timeit.timeit(time,number=1),"s")
