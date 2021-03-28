import numpy as np
import matplotlib.pyplot as plt
from location import Location
from link import Link
from typing import List, Dict

size_mark_stations = 500
size_mark_beacons = 100

plt.style.use('seaborn-whitegrid')
plt.ion()
plt.show()

# stations coordinates
x_stations = [0,0,5,5]
y_stations = [0,5,0,5]

def show(locations: Dict[str, Location]):
    if (locations is not None):
        x_beacons = []
        y_beacons = []
        labels = []
        for key, value in locations.items():
            x_beacons.append(value.x)
            y_beacons.append(value.y)
            labels.append(key)

        #plt.clf()        
        plt.scatter(x_stations, y_stations, s=size_mark_stations, c='red', label='stations')
        plt.scatter(x_beacons, y_beacons, marker='^', s=size_mark_beacons, c='blue', label='beacons')

        plt.axis([0, 5, 0, 5])
        plt.xlabel('Position(x)')
        plt.ylabel('Position(y)')        
        
        fig = plt.gcf()
        fig.canvas.set_window_title('Indoor Position System')
        plt.plot(x_beacons, y_beacons)
        plt.draw()
        plt.pause(0.001)
        #plt.savefig('ScatterPlot_01.png')
